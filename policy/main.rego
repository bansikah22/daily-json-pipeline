package main

# Deny if an image comes from an untrusted registry
deny[msg] {
    input.kind == "CronJob"
    container := input.spec.jobTemplate.spec.template.spec.containers[_]
    allowed_registries := ["bansikah/"]
    
    not image_is_from_allowed_registry(container.image, allowed_registries)
    
    msg := sprintf("CronJob ''%v'' has an untrusted image ''%v''. Allowed registries are: %v", [input.metadata.name, container.image, allowed_registries])
}

# Helper function to check if the image comes from any of the allowed registries
image_is_from_allowed_registry(image, registries) {
    startswith(image, registries[_])
}


