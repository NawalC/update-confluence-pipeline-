# update-confluence-pipeline-

![alt text](image.png)
https://nwalcareem.atlassian.net/wiki/spaces/MFS/pages/229377/Tekton+Test+Page

## Purpose

The purpose of this project is to automate the process of updating Confluence pages with data from various sources. This helps in maintaining up-to-date documentation and streamlining the workflow for teams using Confluence.

## Journey

The journey of this project began with the need to ensure that our Confluence pages reflect the latest information without manual intervention. The project leverages Python scripts to fetch data, process it, and update specific Confluence pages. Over time, the pipeline has been enhanced to handle various data sources and formats, improving its robustness and flexibility.

## Setup and Execution

Follow these steps to set up and execute the pipeline:

1. **Start Minikube**
   ```sh
   minikube start

   
This command starts a local Kubernetes cluster using Minikube.

Use Minikube context

sh
kubectl config use-context minikube
This command sets the current context to Minikube.

Install Tekton Pipelines

sh
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
This command installs the latest Tekton Pipelines on the Kubernetes cluster.

Apply the task configuration

sh
kubectl apply -f task.yaml -n default
This command applies the task.yaml configuration in the default namespace.

Apply the pipeline run configuration

sh
kubectl apply -f pipeline-run.yaml -n default
This command applies the pipeline-run.yaml configuration in the default namespace.

Get the status of the task runs

sh
kubectl get taskruns -n default
This command retrieves the status of the task runs in the default namespace.

View logs of the task run

sh
kubectl logs -n default update-confluence-run-update-page --all-containers
This command retrieves the logs of the task run named update-confluence-run-update-page in the default namespace.

Describe the task run

sh
kubectl describe taskrun update-confluence-run-update-page -n default
This command provides detailed information about the task run named update-confluence-run-update-page in the default namespace.

Get the status of the pods

sh
kubectl get pods -n default
This command retrieves the status of the pods in the default namespace.

View logs of a specific pod step

sh
kubectl logs -n default update-confluence-run-update-page-pod -c step-run-python
This command retrieves the logs of the specific step step-run-python in the pod update-confluence-run-update-page-pod in the default namespace.

Create a secret for Confluence credentials

sh
kubectl create secret generic confluence-creds \
  --from-literal=url=https://nwalcareem.atlassian.net/wiki \
  --from-literal=user=nwal.careem@gmail.com \
  --from-literal=pat=<your-api-token> \
  -n default
This command creates a secret named confluence-creds with the Confluence URL, user, and personal access token (PAT) in the default namespace.
