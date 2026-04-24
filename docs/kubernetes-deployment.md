# Kubernetes Deployment

This guide explains how to deploy the daily data pipeline to a Kubernetes cluster.

## Prerequisites

- A running Kubernetes cluster. This can be a local cluster like `kind` or `minikube`, or a managed cloud cluster.
- `kubectl` configured to connect to your cluster.
- A PersistentVolume provisioner that supports `ReadWriteMany` access mode (e.g., NFS, GlusterFS, or a cloud provider's file service). Note that default installations of `kind` and `minikube` may not support this out of the box and might require an addon like an NFS provisioner.

## 0. (Optional) Creating a Local `kind` Cluster

If you don't have a Kubernetes cluster, you can create one locally using [`kind`](https://kind.sigs.k8s.io/).

```bash
# Create a kind cluster
kind create cluster --name data-pipeline

# Set kubectl context to the new cluster
kubectl cluster-info --context kind-data-pipeline
```

**Note on Storage:** The `PersistentVolumeClaim` in this project requires a `ReadWriteMany` access mode. This is not supported by the default `kind` storage provider, but it is required for both the producer and consumer pods to read and write to the same volume.

For a local `kind` test, you must install an additional storage provisioner. The following steps show how to install the NFS Ganesha server and external provisioner using Helm.

### a. Install Helm

If you don't have Helm, [install it from the official website](https://helm.sh/docs/intro/install/).

### b. Add the Helm Repository

Add the Helm repository that contains the NFS provisioner chart.

```bash
helm repo add nfs-ganesha-server-and-external-provisioner https://kubernetes-sigs.github.io/nfs-ganesha-server-and-external-provisioner/
helm repo update
```

### c. Install the NFS Provisioner

Install the provisioner into your `kind` cluster. It's recommended to install it in a dedicated namespace like `nfs-server`.

```bash
helm install nfs-server-provisioner nfs-ganesha-server-and-external-provisioner/nfs-server-provisioner --namespace nfs-server --create-namespace
```

This will deploy the NFS server and the provisioner that can automatically create persistent volumes.

### d. Use the Provided StorageClass

The Helm chart automatically creates a `StorageClass` named `nfs`. The `k8s/pvc.yml` manifest is already configured to use this `storageClassName`. You can now proceed with deploying the application.

## 1. Build and Push Docker Images

Before deploying, you need to build the Docker images and push them to a container registry that your Kubernetes cluster can access.

See the [Dockerization documentation](dockerization.md) for details on building the images. Make sure to tag the images with your registry's username and push them.

Example:
```bash
# Log in to your registry
docker login -u your-username

# Build the images
docker-compose build

# Push the images
docker-compose push
```

The Kubernetes manifests are pre-configured to use the image names `bansikah/java-scraper:1.0` and `bansikah/python-consumer:1.0`. If you used a different name, be sure to update the `image` field in the CronJob manifests.

### c. (For `kind` clusters) Load Images into the Cluster

If you are using a local `kind` cluster, it cannot pull images from your public Docker Hub registry by default. You must load the images you built directly into the cluster from your local Docker daemon:

```bash
# Load the Java scraper image into the 'data-pipeline' kind cluster
kind load docker-image bansikah/java-scraper:1.0 --name data-pipeline

# Load the Python consumer image into the 'data-pipeline' kind cluster
kind load docker-image bansikah/python-consumer:1.0 --name data-pipeline
```

## 2. Deploy to Kubernetes

All the necessary Kubernetes manifests are located in the `k8s/` directory and are managed by Kustomize.

You can deploy the entire application with a single command:

```bash
kubectl apply -k k8s/
```

This will create the namespace, the persistent volume claim, and both cronjobs in the correct order.

**Note on Testing Schedule:** The CronJobs are currently configured to run every two minutes for testing purposes. To revert to the daily schedule, change the `schedule` field in `k8s/scraper-cronjob.yml` to `"0 2 * * *"` and in `k8s/consumer-cronjob.yml` to `"15 2 * * *"`.

## 3. Verify the Deployment and View Logs

The CronJobs are configured to keep pods for 5 minutes after they complete, giving you plenty of time to inspect their logs.

### a. Watch for Jobs and Pods

You can watch the jobs and pods being created in a new terminal:

```bash
# Watch for jobs to be created by the CronJobs
kubectl get jobs -n data-pipeline -w

# In another terminal, watch the pods
kubectl get pods -n data-pipeline -w
```

### b. View Logs of Completed Jobs

Once a job is complete, you can view its logs directly using the job's name. This is the most reliable method.

```bash
# 1. Get the list of recent jobs
kubectl get jobs -n data-pipeline

# 2. Use the job name in a label selector to get the logs from its pod.
# (replace with a real job name from the list)
kubectl logs -n data-pipeline -l job-name=<job-name-here>

# Example for a specific scraper job:
kubectl logs -n data-pipeline -l job-name=java-scraper-cronjob-29617374

# Example for a specific consumer job:
kubectl logs -n data-pipeline -l job-name=python-consumer-cronjob-29617375
```
This is the most straightforward and reliable way to see the output from your pipeline runs.

You can also follow the logs of a *new* job as it's running. The `kubectl logs -f` command can directly target the CronJob resource. It will wait for the next scheduled job to start and then automatically stream the logs from the pod that gets created.

This is the most reliable way to see the logs in real-time:

```bash
# Follow the logs for the next run of the java-scraper
kubectl logs -f -n data-pipeline cronjob/java-scraper-cronjob

# Follow the logs for the next run of the python-consumer
kubectl logs -f -n data-pipeline cronjob/python-consumer-cronjob
```
```

The pipeline is now deployed to Kubernetes and will run automatically on the schedule defined in the CronJob manifests (daily at 2:00 AM and 2:15 AM).
