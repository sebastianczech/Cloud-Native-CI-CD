# Cloud-Native-CI-CD

Example of continuous integration and deploy pipelines, configuration and code for simple cloud native application.

## Prerequisites

### Install ``diagrams`` tools

```bash
python3 -m venv venv
source venv/bin/activate

pip install diagrams

brew install graphviz
```

### Install ``boto3``

```bash
pip install boto3
```

### Install ``localstack``

```bash
pip install localstack
pip install localstack-client
```

### Install ``pytest``

```bash
pip install pytest
```

### Freeze installed packages

```bash
pip freeze > requirements.txt
```

### TektonCD

Install [Tekton](https://tekton.dev/docs/getting-started/):

```bash
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
kubectl get pods --namespace tekton-pipelines
```

Install Tekton CLI:

```bash
brew tap tektoncd/tools
brew install tektoncd/tools/tektoncd-cli
```

## Design

### Generate pictures from code

```bash
cd design
python cloud_native_ci.py
python cloud_native_cd.py
```

### Continuous integration pipeline

![Continuous integration pipeline](design/cloud_native_ci.png "Continuous integration pipeline")

### Continuous deployment pipeline

![Continuous deployment pipeline](design/cloud_native_cd.png "Continuous deployment pipeline")

## Infrastructure

### Pipeline - continuous integration

#### GitHub actions

![GitHub actions](images/github_actions.png "GitHub actions")

#### GitHub secrets

![GitHub secrets](images/github_secrets.png "GitHub secrets")

#### Docker Hub tokens

![Docker Hub tokens](images/docker_hub_tokens.png "Docker Hub tokens")

### Pipeline - continuous deployment

Prepare namespace:

```
kubectl create namespace cloud-native-app
kubens cloud-native-app
```

Install referenced tasks for [cloning git repositories](https://hub.tekton.dev/tekton/task/git-clone):

```
kubectl apply -f https://raw.githubusercontent.com/tektoncd/catalog/main/task/git-clone/0.4/git-clone.yaml -n cloud-native-app
```

Create tasks:

```bash
kubectl apply -f infra/pipelines -n cloud-native-app
```

Show task:

```bash
tkn task list -n cloud-native-app

tkn task start pull-docker-image --dry-run -n cloud-native-app
```

Start task:

```bash
tkn task start pull-docker-image -n cloud-native-app
```

Check logs:

```bash
tkn taskrun logs pull-docker-image-run-mpkms -f -n cloud-native-app
tkn taskrun logs --last -f -n cloud-native-app
```

Show dashboard:

```bash
kubectl apply --filename https://github.com/tektoncd/dashboard/releases/latest/download/tekton-dashboard-release.yaml
kubectl proxy --port=8080
```

Access dashboard [localhost:8080/api/v1/namespaces/cloud-native-app/services/tekton-dashboard:http/proxy/](http://localhost:8080/api/v1/namespaces/cloud-native-app/services/tekton-dashboard:http/proxy/) or use port forwarding to access dashboard on [localhost:9097](http://localhost:9097):

```bash
kubectl --namespace tekton-pipelines port-forward svc/tekton-dashboard 9097:9097
```

Using [Tekton Pipelines Tutorial](https://github.com/tektoncd/pipeline/blob/main/docs/tutorial.md) and [Build and deploy a Docker image on Kubernetes using Tekton Pipelines](https://developer.ibm.com/tutorials/build-and-deploy-a-docker-image-on-kubernetes-using-tekton-pipelines/) it was prepared whole CD pipeline.

After every change of pipeline, definition needs to be update:

```bash
kubectl apply -f infra/pipelines -n cloud-native-app
```

Pipeline can be started:

```bash
tkn pipeline start pipeline-cd-app -n cloud-native-app --use-param-defaults --workspace name=shared-data,claimName=pvc-pipelines,subPath=dir
```

Clean tasks and runs:

```bash
tkn pipelinerun delete --all -f
tkn pipeline delete --all -f
tkn taskrun delete --all -f
tkn task delete --all -f
```

Remove namespace:

```bash
kubectl delete namespace cloud-native-app
```

### Localstack

Start AWS services on local machine:

```bash
cd infra/localstack
docker-compose up
```

Test localstack:

```bash
pytest test_localstack.py
```

### Terraform

Provision DynamoDB and S3:

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply --auto-approve
```

Check DynamoDB:

```bash
aws --endpoint-url=http://localhost:4566 dynamodb list-tables

aws --endpoint-url http://localhost:4566 dynamodb scan --table-name demo-dynamodb-tf
```

Create S3 bucket and check it:

```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://demo-bucket-cli
aws --endpoint-url=http://localhost:4566 s3api put-bucket-acl --bucket demo-bucket-cli --acl public-read

aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 s3 ls s3://demo-bucket-cli
```

## Application

### Running

```bash
cd app/src
python main.py
LOCALSTACK_HOST=192.168.0.106 python main.py # connect to different Localstack host
```

### Containerization

```bash
docker build --tag python-localstack-client -f app/Dockerfile .
docker run --name python-localstack-client --rm python-localstack-client
docker run --name python-localstack-client --rm -it -e LOCALSTACK_HOST=192.168.0.106 python-localstack-client # change Localstack host
docker run --name python-localstack-client --rm -it python-localstack-client bash # run bash instead of command
```

### Testing

```bash
cd app
pytest tests
pytest -s tests # print to console
INFRA_LOCALSTACK_PROTOCOL=http INFRA_LOCALSTACK_ADDRESS=127.0.0.1 INFRA_LOCALSTACK_PORT=4566 pytest tests
```