package main

# Deny if an image comes from an untrusted registry
deny[msg] {
    input.kind == "CronJob"
    container := input.spec.jobTemplate.spec.template.spec.containers[_]
    allowed_registries := ["bansikah/"]
    not startswith(container.image, allowed_registries[_])
    msg := sprintf("CronJob %v has an untrusted image %v. Allowed registries are: %v", [input.metadata.name, container.image, allowed_registries])
}

