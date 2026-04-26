# Multi-Pod PVC Demo: Sharing a Persistent Volume Between Separate Pods

This example demonstrates the most powerful feature of `ReadWriteMany` volumes: the ability for multiple, independent Pods to mount and interact with the same persistent storage simultaneously. This pattern is the foundation of our main data pipeline.

## How it Works

This setup consists of three separate components:

1.  **`pvc.yml`**: This manifest creates a `PersistentVolumeClaim` named `multi-pod-shared-pvc`. Critically, its `accessModes` is set to `ReadWriteMany`, which is required for more than one pod to mount it. It requests storage from our `nfs` storage class.

2.  **`writer-pod.yml`**:
    -   This Pod mounts the `multi-pod-shared-pvc` at `/data`.
    -   Its only job is to write a message to a file named `multi-pod-message.txt` on the shared volume.

3.  **`reader-pod.yml`**:
    -   This is a **completely separate Pod** that runs at the same time.
    -   It also mounts the *exact same* `multi-pod-shared-pvc`, also at `/data`.
    -   Its command will wait in a loop until it sees the `multi-pod-message.txt` file, at which point it will read the content and print it to its logs.

This demonstrates a true decoupled architecture where two applications communicate asynchronously through a shared filesystem, without needing to know anything about each other directly.

## How to Run

1.  **Apply all the Manifests:**
    ```bash
    # This will create the PVC and both pods
    kubectl apply -f k8s-play/multi-pod-pvc/
    ```

2.  **Verify the Interaction:**
    ```bash
    # Watch the pods start up. They will both go into the 'Running' state.
    kubectl get pods -w

    # Check the logs of the reader pod. After a moment, it will print the message
    # written by the writer pod.
    kubectl logs multi-pvc-reader
    ```

3.  **Clean Up:**
    ```bash
    kubectl delete -f k8s-play/multi-pod-pvc/
    ```
