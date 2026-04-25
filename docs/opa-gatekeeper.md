# OPA Gatekeeper Integration

This document explains how to set up OPA (Open Policy Agent) Gatekeeper to enforce custom policies on your Kubernetes cluster.

## What is Gatekeeper?

Gatekeeper is a policy engine for Kubernetes that allows you to enforce rules and best practices. It acts as an admitting webhook, meaning it can validate, mutate, or reject API requests before they are persisted as objects in the cluster.

For this project, we will use it to create a policy that ensures all container images are pulled from a trusted registry (your `bansikah` Docker Hub repository).

## 1. Installing Gatekeeper

The recommended way to install Gatekeeper is by applying its official release manifests.

```bash
# This command will deploy Gatekeeper to your cluster in the `gatekeeper-system` namespace.
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.11/deploy/gatekeeper.yaml
```

After a few moments, you can verify that the Gatekeeper pods are running:

```bash
kubectl get pods -n gatekeeper-system
```
You should see pods for `gatekeeper-audit` and `gatekeeper-controller-manager`.

## 2. Applying Policies

Once Gatekeeper is running, you can start defining policies. This is done in two parts:
-   **ConstraintTemplate:** A template that defines the logic of a policy.
-   **Constraint:** An instance of a template with specific parameters.

We will create these in the `k8s/policies/` directory.
