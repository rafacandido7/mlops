# 🚧 Backlog Detalhado do Projeto MLOps (Foco em Metaflow UI, Spark MLlib, Sem Monitoramento Avançado) 🚧

## Épico 1: 🏗️ Configuração da Infraestrutura Kubernetes com K3s e Rancher

### Tarefa 1.1: Preparação do Ambiente de Virtualização (Ex: Proxmox)
- [ ] **1.1.1:** Definir especificações das VMs:
    - [ ] VM Rancher Server: Mínimo 2 vCPU, 4GB RAM, 20GB Disco.
    - [ ] VM K3s Server: Mínimo 2 vCPU, 4GB RAM, 20GB Disco.
    - [ ] VM(s) K3s Agent(s) (mínimo 1, recomendado 2 para HA simulado): Mínimo 2 vCPU, 4GB RAM, 20GB Disco cada.
- [ ] **1.1.2:** Criar e configurar VM para Rancher Server:
    - [ ] Instalar SO (Ubuntu Server 22.04 LTS recomendado).
    - [ ] Realizar atualizações: `sudo apt update && sudo apt upgrade -y`.
    - [ ] Configurar IP estático (ou reserva DHCP) e hostname.
    - [ ] Habilitar e configurar acesso SSH.
    - [ ] Instalar Docker: `curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh`.
- [ ] **1.1.3:** Criar e configurar VM para K3s Server:
    - [ ] Instalar SO (Ubuntu Server 22.04 LTS recomendado).
    - [ ] Realizar atualizações.
    - [ ] Configurar IP estático (ou reserva DHCP) e hostname.
    - [ ] Habilitar e configurar acesso SSH.
- [ ] **1.1.4:** Criar e configurar VM(s) para K3s Agent(s):
    - [ ] Instalar SO (Ubuntu Server 22.04 LTS recomendado) em cada VM de agente.
    - [ ] Realizar atualizações em cada VM.
    - [ ] Configurar IP estático (ou reserva DHCP) e hostname em cada VM.
    - [ ] Habilitar e configurar acesso SSH em cada VM.

### Tarefa 1.2: Instalação e Configuração do K3s
- [ ] **1.2.1:** Escolher a versão estável mais recente do K3s.
- [ ] **1.2.2:** Instalar K3s no nó servidor:
    - [ ] Executar comando de instalação (ex: `curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644`).
    - [ ] Verificar status do serviço K3s: `sudo systemctl status k3s`.
    - [ ] Obter o token de join do servidor: `sudo cat /var/lib/rancher/k3s/server/node-token`.
- [ ] **1.2.3:** Instalar K3s nos nós agentes:
    - [ ] Em cada nó agente, executar comando de instalação com token e URL do servidor (ex: `curl -sfL https://get.k3s.io | K3S_URL=https://<IP_DO_SERVIDOR_K3S>:6443 K3S_TOKEN=<TOKEN_DO_SERVIDOR> sh -`).
- [ ] **1.2.4:** Validar a saúde do cluster K3s:
    - [ ] No servidor K3s, copiar config: `mkdir ~/.kube; sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config; sudo chown $(id -u):$(id -g) ~/.kube/config`.
    - [ ] Verificar nós: `kubectl get nodes -o wide`.
    - [ ] Verificar status dos componentes: `kubectl get pods -A`.
- [ ] **1.2.5:** (Opcional) Configurar `kubectl` localmente na sua máquina de desenvolvimento para acessar o cluster K3s remoto (copiar `~/.kube/config` do servidor K3s).

### Tarefa 1.3: Instalação e Configuração do Rancher
- [ ] **1.3.1:** Instalar Rancher Server na VM dedicada usando Docker:
    - [ ] Comando: `sudo docker run -d --restart=unless-stopped -p 80:80 -p 443:443 --privileged rancher/rancher:latest` (verificar tag estável recomendada).
- [ ] **1.3.2:** Acessar a UI do Rancher (https://IP_VM_RANCHER) e:
    - [ ] Obter a senha de bootstrap: `sudo docker logs <ID_CONTAINER_RANCHER> 2>&1 | grep "Bootstrap Password:"`.
    - [ ] Definir nova senha de administrador.
    - [ ] Concordar com os termos e salvar a URL do Rancher.
- [ ] **1.3.3:** Importar o cluster K3s existente para o Rancher:
    - [ ] Na UI do Rancher, ir para "Cluster Management" -> "Import Existing".
    - [ ] Dar um nome ao cluster.
    - [ ] Copiar o comando `kubectl apply -f <URL_DE_REGISTRO>` fornecido pelo Rancher.
    - [ ] Executar o comando no nó servidor K3s (que tem acesso `kubectl` ao cluster).
    - [ ] Aguardar o cluster aparecer como "Active" no Rancher.
- [ ] **1.3.4:** Explorar a UI do Rancher e familiarizar-se com o gerenciamento do cluster K3s importado.

### Tarefa 1.4: Configuração de Namespaces via Rancher/kubectl
- [ ] **1.4.1:** Criar namespace `metaflow`.
- [ ] **1.4.2:** Criar namespace `spark-operator`.
- [ ] **1.4.3:** Criar namespace `minio`.
- [ ] **1.4.4:** Criar namespace `harbor`.
- [ ] **1.4.5:** Criar namespace `cert-manager` (para o cert-manager).
- [ ] **1.4.6:** Criar namespace `longhorn-system` (se for usar Longhorn).
- [ ] **1.4.7:** (Opcional) Criar namespace `postgres` (se for hospedar o PostgreSQL para o Metaflow).

### Tarefa 1.5: Configuração de Ingress e TLS
- [ ] **1.5.1:** Validar funcionamento do Traefik (Ingress Controller padrão do K3s) ou decidir usar NGINX Ingress Controller.
    - [ ] Se optar por NGINX, instalar via Rancher "Apps & Marketplace" no namespace apropriado (ex: `ingress-nginx`).
- [ ] **1.5.2:** Instalar cert-manager via Rancher "Apps & Marketplace" no namespace `cert-manager`.
    - [ ] Manter a opção de instalar CRDs marcada.
- [ ] **1.5.3:** Configurar um `ClusterIssuer` para Let's Encrypt (produção) ou self-signed (desenvolvimento/testes):
    - [ ] Para Let's Encrypt (Staging primeiro, depois Prod): Criar YAML do `ClusterIssuer` (ex: `letsencrypt-staging`, `letsencrypt-prod`) com seu email e o solver HTTP01. Aplicar via `kubectl apply -f <arquivo.yaml>`.
    - [ ] Para Self-Signed: Criar YAML do `ClusterIssuer` (ex: `selfsigned-issuer`). Aplicar via `kubectl`.
- [ ] **1.5.4:** Testar o `ClusterIssuer` criando um certificado para um serviço de exemplo ou para o próprio Rancher UI (se exposto via Ingress).

### Tarefa 1.6: Configuração de Storage
- [ ] **1.6.1:** Avaliar o Local Path Provisioner do K3s:
    - [ ] Verificar se é a `StorageClass` padrão: `kubectl get sc`.
    - [ ] Entender suas limitações (não replicado, vinculado ao nó).
- [ ] **1.6.2:** (Recomendado para maior robustez) Instalar Longhorn via Rancher "Apps & Marketplace" no namespace `longhorn-system`.
    - [ ] Explorar a UI do Longhorn após a instalação.
    - [ ] Definir Longhorn como a `StorageClass` padrão (se desejado, editando a anotação da SC).
    - [ ] Testar: Criar um PVC usando a `StorageClass` do Longhorn, criar um Pod que monte este PVC, escrever dados e verificar a persistência e replicação (se configurada).
- [ ] **1.6.3:** Se optar por manter o Local Path Provisioner, garantir que ele é a `StorageClass` padrão ou especificar seu nome nos PVCs.

### Tarefa 1.7: Instalação e Configuração do Harbor (Repositório de Imagens)
- [ ] **1.7.1:** Instalar Harbor via Helm Chart (Rancher "Apps & Marketplace") no namespace `harbor`.
    - [ ] Configurar `values.yaml` (ou opções na UI do Rancher):
        - Definir `expose.type` como `ingress`.
        - Configurar `expose.ingress.hosts.core` (ex: `harbor.meudominio.com`).
        - Configurar `expose.ingress.className` (para Traefik ou Nginx).
        - Habilitar TLS no Ingress: `expose.ingress.tls.enabled=true`, `expose.ingress.tls.certManager=true`, `expose.ingress.tls.clusterIssuer=<NOME_DO_SEU_CLUSTERISSUER>`.
        - Configurar senhas de administrador (`adminPassword`).
        - Configurar persistência para todos os componentes do Harbor (Registry, Chartmuseum, Jobservice, Database) usando a `StorageClass` do Longhorn (ou outra escolhida).
- [ ] **1.7.2:** Acessar a UI do Harbor e:
    - [ ] Fazer login com o usuário `admin` e a senha definida.
    - [ ] Criar um projeto (ex: `mlops-pipelines`). Marcar como público ou privado conforme necessidade.
- [ ] **1.7.3:** Testar o login no Harbor via Docker CLI: `docker login harbor.meudominio.com`.
- [ ] **1.7.4:** Criar um Kubernetes Secret do tipo `docker-registry` no namespace `metaflow` (e outros se necessário) para autenticação com o Harbor:
    - `kubectl create secret docker-registry harbor-creds --namespace metaflow --docker-server=harbor.meudominio.com --docker-username=admin --docker-password='<SENHA_ADMIN_HARBOR>' --docker-email='<SEU_EMAIL>'`

## Épico 2: 🐳 Preparação da Imagem Docker Customizada

### Tarefa 2.1: Criação do Dockerfile Detalhado
- [ ] **2.1.1:** Escolher imagem base Python (ex: `python:3.10-slim-bullseye`).
- [ ] **2.1.2:** Instalar dependências do sistema (ex: `build-essential`, `curl`, `git`, `openjdk-11-jre-headless` se necessário para Spark).
- [ ] **2.1.3:** Configurar ambiente (ex: `ENV PYTHONUNBUFFERED=1`).
- [ ] **2.1.4:** Instalar Metaflow e plugin Kubernetes: `pip install metaflow[kubernetes]==<VERSAO_METAFLOW>`.
- [ ] **2.1.5:** Instalar PySpark (que inclui MLlib): `pip install pyspark==<VERSAO_SPARK>`.
- [ ] **2.1.6:** Instalar bibliotecas de S3 para Spark/Hadoop e manipulação de dados: `pandas pyarrow boto3`.
    - *Nota: `hadoop-aws` e `aws-java-sdk-bundle` são geralmente baixados pelo Spark em tempo de execução via `spark.jars.packages` ou precisam ser adicionados manualmente ao classpath do Spark na imagem. A abordagem de `spark.jars.packages` no código PySpark é geralmente mais fácil de gerenciar.*
- [ ] **2.1.7:** Instalar outras bibliotecas Python necessárias: `great_expectations==<VERSAO_GE>`.
- [ ] **2.1.8:** Copiar scripts ou arquivos de configuração necessários para a imagem.
- [ ] **2.1.9:** Definir `WORKDIR` e `USER` (se não for root).

### Tarefa 2.2: Build, Teste e Push da Imagem Docker
- [ ] **2.2.1:** Construir a imagem localmente, usando uma tag específica (ex: `metaflow-custom-spark-ml:0.1.0`): `docker build -t harbor.meudominio.com/mlops-pipelines/metaflow-custom-spark-ml:0.1.0 .`
- [ ] **2.2.2:** Testar a imagem localmente:
    - Executar um container: `docker run -it --rm harbor.meudominio.com/mlops-pipelines/metaflow-custom-spark-ml:0.1.0 bash`.
    - Dentro do container, testar imports: `python -c "import metaflow; import pyspark; from pyspark.ml import Pipeline; import great_expectations; import boto3; print('OK')"`.
- [ ] **2.2.3:** Fazer login no Harbor (se a sessão expirou): `docker login harbor.meudominio.com`.
- [ ] **2.2.4:** Enviar a imagem para o Harbor: `docker push harbor.meudominio.com/mlops-pipelines/metaflow-custom-spark-ml:0.1.0`.
- [ ] **2.2.5:** (Opcional) Enviar também com a tag `latest`:
    - `docker tag harbor.meudominio.com/mlops-pipelines/metaflow-custom-spark-ml:0.1.0 harbor.meudominio.com/mlops-pipelines/metaflow-custom-spark-ml:latest`
    - `docker push harbor.meudominio.com/mlops-pipelines/metaflow-custom-spark-ml:latest`
- [ ] **2.2.6:** Verificar se a imagem e as tags estão disponíveis na UI do Harbor no projeto `mlops-pipelines`.

## Épico 3: ⚙️ Deploy dos Serviços Essenciais via Helm (Rancher Apps)

### Tarefa 3.1: Deploy do MinIO
- [ ] **3.1.1:** Preparar configurações para o chart Helm do MinIO (via UI do Rancher Apps ou `values.yaml`):
    - Namespace: `minio`.
    - `accessKey`: Definir uma chave de acesso segura (ex: `minioadmin`).
    - `secretKey`: Definir uma chave secreta segura (ex: `minioadmin123`).
    - `persistence.enabled=true`, `persistence.storageClass=<NOME_DA_STORAGECLASS_LONGHORN_OU_LOCALPATH>`, `persistence.size=50Gi` (ajustar tamanho).
    - `ingress.enabled=true`, `ingress.hosts[0].name=minio.meudominio.com`, `ingress.tls[0].secretName=minio-tls` (o cert-manager criará isso), `ingress.tls[0].hosts[0]=minio.meudominio.com`, `ingress.annotations."cert-manager.io/cluster-issuer"=<NOME_DO_CLUSTERISSUER>`.
    - `service.type=ClusterIP`.
- [ ] **3.1.2:** Deployar MinIO via Rancher "Apps & Marketplace".
- [ ] **3.1.3:** Criar Kubernetes Secret `minio-creds` no namespace `metaflow`:
    - `kubectl create secret generic minio-creds --namespace metaflow \
      --from-literal=MINIO_ENDPOINT_URL='http://minio.minio.svc.cluster.local:9000' \
      --from-literal=MINIO_ACCESS_KEY_ID='<ACCESS_KEY_DEFINIDA_ACIMA>' \
      --from-literal=MINIO_SECRET_ACCESS_KEY='<SECRET_KEY_DEFINIDA_ACIMA>'`
- [ ] **3.1.4:** Acessar a UI do MinIO (https://minio.meudominio.com) e:
    - Fazer login com as credenciais definidas.
    - Criar buckets: `raw-data`, `metaflow-datastore`, `spark-ml-models`, `ge-validations`.

### Tarefa 3.2: Deploy do Spark Operator
- [ ] **3.2.1:** Adicionar o repositório do Helm Chart do Spark Operator ao Rancher, se necessário (ex: `https://googlecloudplatform.github.io/spark-on-k8s-operator`).
- [ ] **3.2.2:** Preparar configurações para o chart do Spark Operator:
    - Namespace: `spark-operator`.
    - `sparkJobNamespace=metaflow` (ou o namespace onde os jobs Spark do Metaflow rodarão).
    - `enableWebhook=true` (geralmente recomendado).
    - Configurar RBAC (geralmente habilitado por padrão).
- [ ] **3.2.3:** Deployar o Spark Operator via Rancher "Apps & Marketplace".
- [ ] **3.2.4:** Validar a instalação:
    - `kubectl get pods -n spark-operator`.
    - `kubectl get crd | grep sparkapplication`.

### Tarefa 3.3: Deploy do Backend de Metadados para Metaflow (PostgreSQL)
- [ ] **3.3.1:** (Opcional, mas recomendado para Metaflow UI e persistência robusta) Deployar PostgreSQL:
    - Usar o chart do Bitnami PostgreSQL via Rancher "Apps & Marketplace" no namespace `postgres` (ou `metaflow`).
    - Configurar:
        - `auth.username=metaflow_user`.
        - `auth.password=<SENHA_SEGURA_PG_METAFLOW>`.
        - `auth.database=metaflow_db`.
        - `primary.persistence.enabled=true`, `primary.persistence.storageClass=<NOME_DA_STORAGECLASS>`, `primary.persistence.size=10Gi`.
- [ ] **3.3.2:** Anotar as credenciais e o nome do serviço do PostgreSQL (ex: `postgres-postgresql.postgres.svc.cluster.local`).

### Tarefa 3.4: Deploy do Metaflow Metadata Service
- [ ] **3.4.1:** Preparar configurações para o chart do Metaflow Metadata Service (pode ser necessário encontrar um chart comunitário ou adaptar um existente):
    - Namespace: `metaflow`.
    - Configuração do backend de metadados:
        - `METADATA_DB_TYPE=postgres`
        - `METADATA_DB_HOST=<NOME_SERVICO_POSTGRESQL>` (ex: `postgres-postgresql.postgres.svc.cluster.local`)
        - `METADATA_DB_PORT=5432`
        - `METADATA_DB_USER=metaflow_user`
        - `METADATA_DB_PSWD=<SENHA_SEGURA_PG_METAFLOW>`
        - `METADATA_DB_NAME=metaflow_db`
    - `service.type=ClusterIP`.
- [ ] **3.4.2:** Deployar o Metaflow Metadata Service.
- [ ] **3.4.3:** Expor o serviço via Ingress (se necessário para acesso externo direto, mas geralmente a UI acessa internamente):
    - `ingress.enabled=true`, `ingress.hosts[0].name=metaflow-service.meudominio.com`, etc. (com TLS).

### Tarefa 3.5: Deploy da Metaflow UI
- [ ] **3.5.1:** Preparar configurações para o chart da Metaflow UI:
    - Namespace: `metaflow`.
    - `METAFLOW_SERVICE_URL=http://metaflow-metadata-service.metaflow.svc.cluster.local:<PORTA_DO_SERVICO>` (ajustar nome e porta do serviço de metadados).
    - `ingress.enabled=true`, `ingress.hosts[0].name=metaflow-ui.meudominio.com`, `ingress.tls[0].secretName=metaflow-ui-tls`, `ingress.tls[0].hosts[0]=metaflow-ui.meudominio.com`, `ingress.annotations."cert-manager.io/cluster-issuer"=<NOME_DO_CLUSTERISSUER>`.
- [ ] **3.5.2:** Deployar a Metaflow UI via Rancher "Apps & Marketplace".
- [ ] **3.5.3:** Acessar a Metaflow UI (https://metaflow-ui.meudominio.com) e verificar se está funcionando e conectada ao serviço de metadados (inicialmente não haverá fluxos).

## Épico 4: 🚀 Desenvolvimento do Pipeline Metaflow com Spark MLlib

### Tarefa 4.1: Configuração Inicial do Ambiente e Flow
- [ ] **4.1.1:** Criar diretório do projeto: `mkdir meu_projeto_mlops && cd meu_projeto_mlops`.
- [ ] **4.1.2:** Criar o arquivo `pipeline.py`.
- [ ] **4.1.3:** Configurar o `config.json` do Metaflow localmente (no diretório `~/.metaflowconfig/` ou no diretório do projeto):
    ```json
    {
        "METAFLOW_DATASTORE_SYSROOT_S3": "s3://metaflow-datastore/",
        "METAFLOW_S3_ENDPOINT_URL": "[http://minio.minio.svc.cluster.local:9000](http://minio.minio.svc.cluster.local:9000)",
        "METAFLOW_S3_ACCESS_KEY_ID": "<ACCESS_KEY_MINIO>",
        "METAFLOW_S3_SECRET_ACCESS_KEY": "<SECRET_KEY_MINIO>",
        "METAFLOW_KUBERNETES_DEFAULT_IMAGE": "[harbor.meudominio.com/mlops-pipelines/metaflow-custom-spark-ml:latest](https://harbor.meudominio.com/mlops-pipelines/metaflow-custom-spark-ml:latest)", // Imagem padrão atualizada
        "METAFLOW_KUBERNETES_NAMESPACE": "metaflow",
        "METAFLOW_KUBERNETES_SERVICE_ACCOUNT": "default",
        "METAFLOW_KUBERNETES_SECRETS": "minio-creds",
        "METAFLOW_METADATA_SERVICE_URL": "[http://metaflow-metadata-service.metaflow.svc.cluster.local](http://metaflow-metadata-service.metaflow.svc.cluster.local):<PORTA>"
    }
    ```
- [ ] **4.1.4:** Definir a classe `FlowSpec` básica no `pipeline.py` com `if __name__ == '__main__':`
- [ ] **4.1.5:** Adicionar `Parameters` para o flow (ex: `minio_bucket_raw_data`, `minio_path_raw_data`, `model_output_bucket`).
- [ ] **4.1.6:** Definir constantes para nome da imagem (se não usar default da config) e nome do secret K8s.

### Tarefa 4.2: Implementação do Step `start`
- [ ] **4.2.1:** Criar o método `start(self)`.
- [ ] **4.2.2:** Adicionar decorador `@step`.
- [ ] **4.2.3:** Imprimir mensagens de início e parâmetros do flow.
- [ ] **4.2.4:** Definir `self.next(self.ingest_and_validate_data)`.

### Tarefa 4.3: Implementação do Step `ingest_and_validate_data`
- [ ] **4.3.1:** Criar o método. Adicionar decorador `@kubernetes()`.
- [ ] **4.3.2:** Configurar SparkSession (com acesso ao MinIO e `jars.packages` para S3A).
- [ ] **4.3.3:** Ler dados Parquet do MinIO para um Spark DataFrame.
- [ ] **4.3.4:** Realizar contagem e `df.show(5)`.
- [ ] **4.3.5:** Implementar validação com Great Expectations (usando `SparkDFDataset`).
- [ ] **4.3.6:** Armazenar Spark DataFrame como artefato Metaflow (ou seu path S3): `self.ingested_spark_df_path` (se salvo no S3) ou `self.ingested_spark_df` (se Metaflow puder serializá-lo eficientemente via datastore S3).
- [ ] **4.3.7:** Parar a sessão Spark: `spark.stop()`.
- [ ] **4.3.8:** Definir `self.next(self.preprocess_data)`.

### Tarefa 4.4: Implementação do Step `preprocess_data`
- [ ] **4.4.1:** Criar método. Adicionar decoradores `@kubernetes`.
- [ ] **4.4.2:** Iniciar SparkSession.
- [ ] **4.4.3:** Carregar Spark DataFrame do step anterior.
- [ ] **4.4.4:** Implementar lógica de pré-processamento com transformadores PySpark (ex: `StringIndexer`, `OneHotEncoder`, normalização, tratamento de nulos).
- [ ] **4.4.5:** Armazenar Spark DataFrame processado: `self.processed_spark_df_path` ou `self.processed_spark_df`.
- [ ] **4.4.6:** Parar SparkSession.
- [ ] **4.4.7:** Definir `self.next(self.train_spark_ml_model)`.

### Tarefa 4.5: Implementação do Step `train_spark_ml_model`
- [ ] **4.5.1:** Criar método. Adicionar decoradores `@kubernetes`.
- [ ] **4.5.2:** Iniciar SparkSession.
- [ ] **4.5.3:** Carregar `self.processed_spark_df` (ou ler do `self.processed_spark_df_path`).
- [ ] **4.5.4:** Preparar features para Spark MLlib:
    - Usar `pyspark.ml.feature.VectorAssembler` para combinar colunas de features em uma única coluna `features`.
- [ ] **4.5.5:** Definir o modelo Spark MLlib:
    - Ex: `from pyspark.ml.regression import LinearRegression`
    - `lr = LinearRegression(featuresCol='features', labelCol='<SUA_COLUNA_ALVO>')`
- [ ] **4.5.6:** (Opcional) Criar um `pyspark.ml.Pipeline` do Spark MLlib:
    - `from pyspark.ml import Pipeline`
    - `pipeline = Pipeline(stages=[vector_assembler, lr])`
- [ ] **4.5.7:** Dividir dados em treino e teste (se ainda não feito): `trainingData, testData = processed_df.randomSplit([0.8, 0.2])`.
- [ ] **4.5.8:** Treinar o modelo/pipeline: `spark_model = pipeline.fit(trainingData)`.
- [ ] **4.5.9:** Definir o path de S3 para salvar o modelo: `self.spark_model_s3_path = f"s3a://{self.model_output_bucket}/run_{self.run_id}/spark_ml_model"`.
- [ ] **4.5.10:** Salvar o modelo Spark MLlib treinado no MinIO: `spark_model.save(self.spark_model_s3_path)`.
- [ ] **4.5.11:** Salvar `self.spark_model_s3_path` como artefato Metaflow.
- [ ] **4.5.12:** Armazenar `testData` para o próximo step (ex: `self.test_data_path` se salvar no S3, ou `self.test_data` se for pequeno o suficiente).
- [ ] **4.5.13:** Parar SparkSession.
- [ ] **4.5.14:** Definir `self.next(self.evaluate_spark_ml_model)`.

### Tarefa 4.6: Implementação do Step `evaluate_spark_ml_model`
- [ ] **4.6.1:** Criar método. Adicionar decorador `@kubernetes`.
- [ ] **4.6.2:** Iniciar SparkSession.
- [ ] **4.6.3:** Carregar o modelo Spark MLlib treinado do `self.spark_model_s3_path`:
    - `from pyspark.ml import PipelineModel` (ou o tipo de modelo específico)
    - `loaded_spark_model = PipelineModel.load(self.spark_model_s3_path)`
- [ ] **4.6.4:** Carregar os dados de teste (`self.test_data` ou ler do `self.test_data_path`).
- [ ] **4.6.5:** Fazer predições: `predictions = loaded_spark_model.transform(testData)`.
- [ ] **4.6.6:** Avaliar o modelo usando `Evaluator`s do Spark MLlib:
    - Ex: `from pyspark.ml.evaluation import RegressionEvaluator`
    - `evaluator = RegressionEvaluator(labelCol='<SUA_COLUNA_ALVO>', predictionCol="prediction", metricName="rmse")`
    - `rmse = evaluator.evaluate(predictions)`
    - Salvar métricas (RMSE, R2, etc.) como artefatos Metaflow: `self.model_rmse = rmse`.
- [ ] **4.6.7:** Parar SparkSession.
- [ ] **4.6.8:** Definir `self.next(self.end)`.

### Tarefa 4.7: Implementação do Step `end`
- [ ] **4.7.1:** Criar método. Adicionar decorador `@step`.
- [ ] **4.7.2:** Imprimir mensagem de finalização, métricas principais e o path do modelo salvo no S3 (`self.spark_model_s3_path`).
- [ ] **4.7.3:** (Opcional) Usar `metaflow.cards` para gerar um card de resumo da execução.

### Tarefa 4.8: Testes e Execução do Pipeline
- [ ] **4.8.1:** Preparar dados de exemplo em formato Parquet e fazer upload para o bucket `raw-data` no MinIO.
- [ ] **4.8.2:** Executar o pipeline localmente com o target Kubernetes: `python pipeline.py --environment=conda run --with kubernetes ...`.
- [ ] **4.8.3:** Monitorar os pods dos steps no Rancher UI.
- [ ] **4.8.4:** Verificar logs dos pods.
- [ ] **4.8.5:** Acessar a Metaflow UI para inspecionar a execução, logs e artefatos (incluindo `spark_model_s3_path` e métricas).
- [ ] **4.8.6:** Verificar se o modelo Spark MLlib foi salvo corretamente no bucket `spark-ml-models` no MinIO (será um diretório com metadados e dados do modelo).
- [ ] **4.8.7:** Verificar artefatos do Metaflow no bucket `metaflow-datastore`.
- [ ] **4.8.8:** Iterar e depurar conforme necessário.

## Épico 5: 🧐 Monitoramento Básico e Observabilidade do Pipeline
*(Foco no monitoramento via logs, Rancher UI e Metaflow UI)*
- [ ] **5.1.1:** Definir estratégia de logging consistente para os steps do Metaflow e jobs Spark.
- [ ] **5.1.2:** Utilizar a Rancher UI para monitorar a saúde dos Pods e Deployments dos serviços.
- [ ] **5.1.3:** Utilizar a Metaflow UI extensivamente para observar o status, logs e artefatos dos pipelines.
- [ ] **5.1.4:** Verificar logs dos containers dos serviços principais e dos drivers/executores Spark via `kubectl logs` ou Rancher UI.
- [ ] **5.1.5:** Monitorar o uso de recursos dos nós e pods através da UI do Rancher.

## Épico 6: 🔄 Implementação de CI/CD (Opcional)

### Tarefa 6.1: Pipeline de Integração Contínua (CI) - Ex: GitHub Actions
- [ ] **6.1.1:** Criar workflow YAML em `.github/workflows/ci.yaml`.
- [ ] **6.1.2:** Definir trigger.
- [ ] **6.1.3:** Configurar jobs: checkout, linters, testes unitários (se houver), login no Harbor, build e push da imagem Docker (ex: `metaflow-custom-spark-ml`).

### Tarefa 6.2: Pipeline de Deploy Contínuo (CD) - Ex: GitHub Actions (Simples)
- [ ] **6.2.1:** (Opcional) Adicionar job ao workflow de CI ou criar novo.
- [ ] **6.2.2:** Configurar `kubectl` no runner do CI.
- [ ] **6.2.3:** Lógica para atualizar deployments/jobs (se aplicável, mais relevante para agendadores).

## Épico 7: 📝 Documentação e Testes Finais

### Tarefa 7.1: Documentação do Projeto
- [ ] **7.1.1:** Atualizar `README.md` principal (já feito).
- [ ] **7.1.2:** Documentar processo de setup da infraestrutura.
- [ ] **7.1.3:** Documentar o `Dockerfile` e o processo de build da imagem.
- [ ] **7.1.4:** Documentar o pipeline Metaflow (`pipeline.py`) com foco no uso do Spark MLlib.
- [ ] **7.1.5:** Documentar como executar o pipeline e acessar os resultados.
- [ ] **7.1.6:** (Se CI/CD implementado) Documentar o pipeline de CI/CD.

### Tarefa 7.2: Testes de Ponta a Ponta e Validação Final
- [ ] **7.2.1:** Preparar um conjunto de dados de teste final e representativo.
- [ ] **7.2.2:** Executar o pipeline Metaflow completo.
- [ ] **7.2.3:** Validar outputs: artefatos na Metaflow UI, modelo Spark MLlib no MinIO, logs, métricas.
- [ ] **7.2.4:** Verificar a persistência dos serviços.
- [ ] **7.2.5:** Validar o acesso a todas as UIs via Ingress com TLS.
- [ ] **7.2.6:** Realizar uma revisão de segurança básica.

---