# Debugging and Monitoring the Shared Volume Pod

This guide provides a set of `kubectl` commands to inspect, debug, and monitor the `shared-demo` pod and its shared `emptyDir` volume.

## 1. Check Pod Status and Events

Use these commands to see if the Pod started correctly and if its resource requests were accepted by the cluster.

```bash
# Get the general status of the pod (e.g., Running, Pending, CrashLoopBackOff)
kubectl get pod shared-demo

# Get a detailed view, including recent events, container states, and volume mounts
kubectl describe pod shared-demo
```

## 2. Verify Volume Sharing

Confirm that the `writer` container successfully passed data to the `reader` container through the shared volume.

```bash
# View the logs of the reader container to see if it printed the "hello" message
kubectl logs shared-demo -c reader

# List the files inside the shared directory from the reader's perspective
kubectl exec shared-demo -c reader -- ls -l /shared

# Check the content of the file manually from within the reader container
kubectl exec shared-demo -c reader -- cat /shared/msg.txt
```

## 3. Monitor Resource Usage

See how much CPU and Memory the containers are actually using.
*(Note: This requires the [Metrics Server](https://github.com/kubernetes-sigs/metrics-server) to be installed in your cluster).*

```bash
# Get a summary of the Pod's total resource usage
kubectl top pod shared-demo

# Get a breakdown of resource usage for both the 'writer' and 'reader' containers
kubectl top pod shared-demo --containers
```

## 4. Debugging Common Failures

If the Pod isn't working as expected, use these commands to diagnose specific issues.

```bash
# Check if a container was killed for using too much memory (OOMKilled)
kubectl get pod shared-demo -o jsonpath='{.status.containerStatuses[*].lastState.terminated.reason}'

# Watch the Pod in real-time to see if it restarts unexpectedly
kubectl get pod shared-demo --watch
```

## Understanding the YAML Manifest

The magic of sharing files between containers happens in two key sections of the `share-dir-pod.yaml` manifest: `volumes` and `volumeMounts`.

```yaml
# share-dir-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: shared-demo
spec:
  containers:
  - name: writer
    image: busybox
    command: ["sh","-c","echo hello > /shared/msg.txt && sleep 3600"]
    # 2. This section makes the volume available INSIDE the container.
    volumeMounts:
    - name: shared-vol
      mountPath: /shared

  - name: reader
    image: busybox
    command: ["sh","-c","cat /shared/msg.txt && sleep 3600"]
    # Both containers mount the SAME volume by name.
    volumeMounts:
    - name: shared-vol
      mountPath: /shared

  # 1. This section defines a volume for the entire Pod.
  volumes:
  - name: shared-vol
    emptyDir: {}
```

### 1. The `volumes` Section (Pod-Level)

-   **Purpose:** The `volumes` list defines a storage volume that is available to *all containers* within the Pod. Think of it as declaring a shared hard drive for the Pod.
-   **`name: shared-vol`**: This gives the volume a unique name within the Pod. This name is how we will refer to it later.
-   **`emptyDir: {}`**: This specifies the *type* of volume. An `emptyDir` is a simple, temporary directory that is created when the Pod starts and is completely erased when the Pod is deleted. It's perfect for sharing temporary files between containers running in the same Pod.

### 2. The `volumeMounts` Section (Container-Level)

-   **Purpose:** The `volumeMounts` section makes a Pod-level volume accessible inside a *specific container's* filesystem.
-   **`name: shared-vol`**: This tells Kubernetes *which* Pod-level volume to mount. It must match the name from the `volumes` list.
-   **`mountPath: /shared`**: This specifies the path inside the container where the `shared-vol` volume will appear.

By having both the `writer` and `reader` containers mount the same volume (`shared-vol`), they are both looking at the exact same directory, which allows them to share files seamlessly.

---

## 5. Resizing a PersistentVolumeClaim (PVC)


The question "Should we look at how to increase the storage size of that PVC if you run out of space?" is a great one. The pod in this example uses an `emptyDir` volume, which is temporary and exists only as long as the pod. It cannot be resized.

However, for a `PersistentVolumeClaim` (PVC) like the one used in our main data pipeline, you can often resize it if the underlying `StorageClass` supports volume expansion.

To do so, you would:
1.  **Edit the PVC manifest:** Change the `spec.resources.requests.storage` value to the new, larger size.
    ```yaml
    # pvc.yml
    ...
    spec:
      resources:
        requests:
          storage: 2Gi # Changed from 1Gi
    ```
2.  **Apply the change:**
    ```bash
    kubectl apply -f pvc.yml
    ```
The volume will then be resized without needing to delete the pod. This feature is controlled by the `allowVolumeExpansion: true` setting in the `StorageClass`.
