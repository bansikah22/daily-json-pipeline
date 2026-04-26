# PVC Demo: Using a PersistentVolumeClaim with a Single Pod

This example demonstrates how to use a `PersistentVolumeClaim` (PVC) to provide persistent storage to a Pod. Unlike an `emptyDir` volume, data written to a PVC will persist even if the Pod is deleted and recreated.

## How it Works

1.  **`pvc.yml`**: This manifest creates a `PersistentVolumeClaim` named `single-pod-pvc`. It requests a small amount of storage (100Mi) from the `nfs` storage class, which is capable of providing `ReadWriteMany` volumes (though only one pod is using it here).

2.  **`pod.yml`**:
    -   Under `spec.volumes`, we define a volume named `my-pvc-storage`.
    -   Instead of using `emptyDir`, its type is `persistentVolumeClaim`, and we specify the `claimName: single-pod-pvc`. This tells the Pod to use the PVC we created.
    -   The `writer` container then mounts this volume at `/data` using `volumeMounts`.

## How to Run

1.  **Apply the Manifests:**
    ```bash
    kubectl apply -f k8s-play/pvc-demo/
    ```

2.  **Verify the Data:**
    ```bash
    # Wait for the pod to be in the 'Running' state
    kubectl get pod pvc-writer-pod

    # Exec into the pod and check the contents of the file
    kubectl exec pvc-writer-pod -- cat /data/pvc-message.txt
    ```

3.  **Test Persistence:**
    ```bash
    # Delete the pod
    kubectl delete pod pvc-writer-pod

    # Recreate the pod
    kubectl apply -f k8s-play/pvc-demo/pod.yml

    # Wait for it to start, then check the file again.
    # The message will still be there!
    kubectl exec pvc-writer-pod -- cat /data/pvc-message.txt
    ```
