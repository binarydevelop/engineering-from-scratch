"""
Project 10: Declarative service.yaml IDP Compiler.
"""
from typing import Dict, Any

def compile_service_yaml(spec: Dict[str, Any]) -> Dict[str, Any]:
    name = spec["name"]
    port = spec.get("port", 8080)
    replicas = spec.get("replicas", 2)
    return {
        "k8s_deployment": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": name},
            "spec": {"replicas": replicas}
        },
        "k8s_service": {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": name},
            "spec": {"ports": [{"port": port, "targetPort": port}]}
        }
    }
