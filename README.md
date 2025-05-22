# Projeto MLOps: Pipeline de Machine Learning com Metaflow e Spark MLlib em K3s

## 📚 Visão Geral

Este projeto implementa um pipeline de Machine Learning de ponta a ponta, utilizando Metaflow para orquestração e **Apache Spark (com MLlib) para processamento de dados distribuído e treinamento de modelos**. Toda a infraestrutura é executada em um cluster K3s, gerenciado via Rancher, com componentes adicionais como Harbor para registro de imagens Docker e MinIO para armazenamento de objetos.

O objetivo é criar um ambiente de MLOps robusto e escalável, adequado para desenvolvimento, experimentação e potencial implantação de modelos de Machine Learning, com foco na arquitetura e infraestrutura e utilizando o poder do Spark de ponta a ponta.

## ✨ Funcionalidades Principais

* **Orquestração de Pipeline com Metaflow:** Definição e execução de fluxos de trabalho de ML complexos.
* **Interface Gráfica do Metaflow (Metaflow UI):** Visualização e inspeção de execuções de pipelines, steps e artefatos.
* **Processamento de Dados com PySpark:** Capacidade de processar grandes volumes de dados (arquivos Parquet) de forma distribuída.
* **Treinamento de Modelos com Spark MLlib:** Treinamento de modelos de Machine Learning diretamente em Spark DataFrames, aproveitando a computação distribuída.
* **Execução em Kubernetes (K3s):** Os steps do Metaflow são executados como pods no K3s, permitindo escalabilidade e isolamento.
* **Gerenciamento Centralizado de Cluster com Rancher:** Facilidade para gerenciar o cluster K3s, namespaces, deployments e outros recursos.
* **Registro Privado de Imagens com Harbor:** Armazenamento seguro e versionamento de imagens Docker customizadas.
* **Armazenamento de Objetos com MinIO:** Utilizado para armazenar dados brutos, datasets processados, artefatos do Metaflow e modelos Spark MLlib treinados.
* **Validação de Dados com Great Expectations:** Garantia da qualidade e integridade dos dados ao longo do pipeline (aplicada em Spark DataFrames).
* **Persistência de Dados Robusta com Longhorn:** Storage distribuído e replicado para os serviços stateful.
* **Gerenciamento de Certificados TLS com Cert-Manager:** Emissão e renovação automática de certificados TLS para os serviços expostos.

## 🛠️ Stack Tecnológica

* **Virtualização:** Proxmox (ou qualquer outro hipervisor/ambiente bare-metal)
* **Sistema Operacional das VMs:** Ubuntu Server 22.04 LTS (recomendado)
* **Orquestração de Containers:** K3s
* **Gerenciamento de Cluster Kubernetes:** Rancher
* **Orquestração de Pipeline ML:** Metaflow
* **Processamento de Dados e Treinamento de Modelos ML:** Apache Spark (PySpark com MLlib)
* **Validação de Dados:** Great Expectations
* **Armazenamento de Objetos:** MinIO
* **Registro de Imagens Docker:** Harbor
* **Storage Distribuído para K8s:** Longhorn
* **Ingress Controller:** Traefik (padrão do K3s) ou NGINX
* **Gerenciamento de Certificados TLS:** Cert-Manager
* **Banco de Dados para Metaflow:** PostgreSQL
* **Linguagem Principal:** Python 3.10+ (com PySpark)
* **Conteinerização:** Docker

## 📋 Pré-requisitos

* Acesso a um ambiente de virtualização (como Proxmox) ou máquinas físicas para as VMs.
* Conhecimento básico de Linux, Docker, Kubernetes e Apache Spark.
* `kubectl` instalado na sua máquina local para interagir com o cluster.
* Conta no Docker Hub (ou outro registro público) se precisar puxar imagens base não disponíveis localmente.
* Um nome de domínio (ou subdomínios) configurado para apontar para o IP do seu Ingress no K3s (para acesso aos serviços com TLS).

## 🚀 Configuração da Infraestrutura e Deploy

A configuração completa da infraestrutura e o deploy dos serviços seguem um processo detalhado. Consulte o arquivo `BACKLOG.md` para um passo a passo minucioso. As etapas principais incluem:

1.  **Preparação das VMs:** Criação e configuração das VMs para Rancher, K3s Server e K3s Agents.
2.  **Instalação do K3s:** Setup do cluster K3s (1 servidor, múltiplos agentes).
3.  **Instalação do Rancher:** Deploy do Rancher Server e importação do cluster K3s.
4.  **Configurações Iniciais no K3s/Rancher:**
    * Criação de Namespaces (`metaflow`, `spark-operator`, `minio`, `harbor`, `cert-manager`, `longhorn-system`, `postgres`).
    * Instalação e configuração do Ingress Controller e Cert-Manager.
    * Instalação e configuração do Longhorn como StorageClass.
5.  **Deploy do Harbor:** Instalação via Helm (Rancher Apps), configuração de Ingress com TLS e persistência.
6.  **Build da Imagem Docker Customizada:**
    * Criação do `Dockerfile` com Python, Metaflow, **PySpark (que inclui MLlib)** e outras dependências.
    * Build e push da imagem para o Harbor.
7.  **Deploy dos Serviços Essenciais via Rancher Apps (Helm):**
    * **MinIO:** Configuração de persistência, credenciais e Ingress. Criação de buckets.
    * **PostgreSQL:** Para o backend de metadados do Metaflow.
    * **Metaflow Metadata Service:** Conectado ao PostgreSQL.
    * **Metaflow UI:** Conectada ao Metadata Service e exposta via Ingress com TLS.
    * **Spark Operator:** Para gerenciar `SparkApplication` (se usado diretamente, ou para referência se o Spark rodar no pod do Metaflow).
8.  **Criação de Secrets Kubernetes:**
    * `harbor-creds`: Para o K3s puxar a imagem customizada do Harbor.
    * `minio-creds`: Para o Metaflow e Spark acessarem o MinIO.

## 🌊 Visão Geral do Pipeline Metaflow (`pipeline.py`)

O pipeline de Machine Learning é orquestrado pelo Metaflow e consiste nos seguintes steps principais, utilizando Spark para processamento e MLlib para treinamento:

1.  **`start`**: Ponto de entrada do pipeline, inicializa parâmetros.
2.  **`ingest_and_validate_data`**:
    * Conecta-se ao MinIO usando PySpark.
    * Lê dados brutos em formato Parquet, resultando em um Spark DataFrame.
    * Valida o Spark DataFrame carregado usando Great Expectations.
    * Armazena o Spark DataFrame validado como um artefato do Metaflow (ou seu path no MinIO).
3.  **`preprocess_data`**:
    * Carrega o Spark DataFrame validado.
    * Realiza etapas de pré-processamento e engenharia de features usando transformadores do PySpark (ex: `StringIndexer`, `OneHotEncoder`, normalização).
    * Armazena o Spark DataFrame processado como um artefato.
4.  **`train_spark_ml_model`**:
    * Carrega o Spark DataFrame processado.
    * Utiliza `VectorAssembler` do Spark MLlib para combinar colunas de features em um único vetor de features.
    * Define um modelo do Spark MLlib (ex: `pyspark.ml.regression.LinearRegression`, `pyspark.ml.classification.RandomForestClassifier`).
    * Opcionalmente, cria um `pyspark.ml.Pipeline` do Spark MLlib incluindo o `VectorAssembler` e o modelo.
    * Treina o modelo/pipeline Spark MLlib (`model = pipeline.fit(trainingData)`).
    * Salva o modelo Spark MLlib treinado diretamente no MinIO (ex: `model.save("s3a://<bucket>/<path>/spark_ml_model")`).
    * Salva o path do modelo no MinIO e metadados relevantes como artefatos do Metaflow.
5.  **`evaluate_model`**:
    * Carrega o modelo Spark MLlib treinado do MinIO.
    * Realiza predições no conjunto de teste (um Spark DataFrame).
    * Avalia o modelo usando `Evaluator`s do Spark MLlib (ex: `RegressionEvaluator`, `BinaryClassificationEvaluator`).
    * Salva as métricas de avaliação como artefatos do Metaflow.
6.  **`end`**: Ponto final do pipeline, loga informações de conclusão e o path do modelo salvo.

## 🏃 Como Executar o Pipeline

1.  **Configure o Ambiente Metaflow Local:**
    * Certifique-se de que o Metaflow está instalado na sua máquina de desenvolvimento.
    * Crie ou atualize seu arquivo `~/.metaflowconfig/config.json` (ou `config.json` no diretório do projeto) para apontar para os serviços no cluster K3s (MinIO como datastore, Metaflow Metadata Service). Veja o exemplo no `BACKLOG.md` (Tarefa 4.1.3).

2.  **Prepare os Dados de Entrada:**
    * Faça upload dos seus arquivos Parquet de dados brutos para o bucket configurado no MinIO (ex: `s3a://raw-data/caminho/para/dados/`).

3.  **Execute o Pipeline:**
    Navegue até o diretório do projeto que contém o arquivo `pipeline.py` e execute:

    ```bash
    python pipeline.py --environment=conda run --with kubernetes \
        --minio_bucket_raw_data=<SEU_BUCKET_RAW_DATA> \
        --minio_path_raw_data=<CAMINHO_DENTRO_DO_BUCKET> \
        --model_output_bucket=<SEU_BUCKET_DE_MODELOS_NO_MINIO> # Onde os modelos Spark serão salvos
    ```
    * Substitua os valores dos parâmetros conforme necessário.
    * O `--environment=conda` é opcional se suas dependências locais estiverem alinhadas com a imagem Docker.
    * A flag `--with kubernetes` instrui o Metaflow a executar os steps como pods no Kubernetes, usando a imagem Docker e configurações definidas.

## 🖥️ Acessando os Serviços

Após o deploy e configuração correta dos Ingresses e DNS, os serviços estarão acessíveis através das seguintes URLs (substitua `meudominio.com` pelo seu domínio configurado):

* **Rancher UI:** `https://rancher.meudominio.com`
* **Harbor UI:** `https://harbor.meudominio.com`
* **MinIO UI:** `https://minio.meudominio.com`
* **Metaflow UI:** `https://metaflow-ui.meudominio.com`

## 🔧 Configurações Importantes

* **Metaflow `config.json`:** Essencial para o cliente Metaflow local se comunicar com os serviços no cluster.
* **Kubernetes Secrets:**
    * `harbor-creds` (namespace `metaflow`): Para que o Kubernetes possa puxar a imagem customizada do seu Harbor privado para os pods dos steps do Metaflow.
    * `minio-creds` (namespace `metaflow`): Para que os steps do Metaflow (rodando como pods com Spark) possam acessar o MinIO para ler dados e salvar artefatos/modelos.

## 📂 Estrutura do Diretório (Sugestão)
```bash
meu_projeto_mlops/
├── pipeline.py             # Script principal do pipeline Metaflow
├── Dockerfile              # Define a imagem customizada para os steps do Metaflow
├── config.json             # Configuração local do Metaflow (pode estar em ~/.metaflowconfig/)
├── requirements.txt        # Dependências Python para ambiente local (opcional)
├── k8s/                    # (Opcional) Manifestos Kubernetes customizados, se houver
│   ├── secrets/
│   └── issuers/
├── notebooks/              # (Opcional) Jupyter notebooks para exploração e análise
├── data/                   # (Opcional) Pequenos datasets de exemplo locais
├── tests/                  # (Opcional) Testes unitários ou de integração
├── README.md               # Este arquivo
└── BACKLOG.md              # Backlog detalhado do projeto
```