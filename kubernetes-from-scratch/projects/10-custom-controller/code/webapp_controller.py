#!/usr/bin/env python3
"""
webapp_controller.py - Custom Controller & Operator Reconciler

Capstone 3 (Phases 84 & 118): Demonstrates Kubernetes extensibility.
Watches a Custom Resource 'WebApp' (learning.example/v1) and reconciles:
  1. An underlying Deployment (managing replicas and image)
  2. An underlying Service (providing stable cluster networking)

Can run directly against a live cluster or in mock/simulation mode.
"""

import sys
import json
import time
import subprocess
from typing import Dict, Any

CRD_MANIFEST = """
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: webapps.learning.example
spec:
  group: learning.example
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                image:
                  type: string
                replicas:
                  type: integer
                text:
                  type: string
                port:
                  type: integer
  scope: Namespaced
  names:
    plural: webapps
    singular: webapp
    kind: WebApp
    shortNames:
    - wa
"""

def generate_deployment_manifest(name: str, namespace: str, image: str, replicas: int, text: str, port: int) -> Dict[str, Any]:
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"{name}-deployment",
            "namespace": namespace,
            "labels": {"app": name, "managed-by": "webapp-controller"}
        },
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [{
                        "name": "web",
                        "image": image or "hashicorp/http-echo:latest",
                        "args": [f"-text={text}"] if text else [],
                        "ports": [{"containerPort": port or 5678}],
                        "resources": {
                            "requests": {"cpu": "50m", "memory": "64Mi"},
                            "limits": {"cpu": "100m", "memory": "128Mi"}
                        }
                    }]
                }
            }
        }
    }

def generate_service_manifest(name: str, namespace: str, port: int) -> Dict[str, Any]:
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": f"{name}-service",
            "namespace": namespace,
            "labels": {"app": name, "managed-by": "webapp-controller"}
        },
        "spec": {
            "type": "ClusterIP",
            "selector": {"app": name},
            "ports": [{
                "name": "http",
                "port": 80,
                "targetPort": port or 5678
            }]
        }
    }

class WebAppReconciler:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

    def reconcile_webapp(self, cr: Dict[str, Any]):
        name = cr["metadata"]["name"]
        namespace = cr["metadata"].get("namespace", "default")
        spec = cr.get("spec", {})

        image = spec.get("image", "hashicorp/http-echo:latest")
        replicas = spec.get("replicas", 2)
        text = spec.get("text", f"Hello from {name}")
        port = spec.get("port", 5678)

        print(f"\n[RECONCILER] Reconciling WebApp '{namespace}/{name}'...")
        print(f"  Target Image    : {image}")
        print(f"  Target Replicas : {replicas}")
        print(f"  Target Port     : {port}")

        dep_manifest = generate_deployment_manifest(name, namespace, image, replicas, text, port)
        svc_manifest = generate_service_manifest(name, namespace, port)

        if self.dry_run:
            print(f"  [DRY RUN] Generated Child Deployment: {dep_manifest['metadata']['name']}")
            print(f"  [DRY RUN] Generated Child Service   : {svc_manifest['metadata']['name']}")
            print("  [SUCCESS] Desired child resources generated correctly!")
            return

        # Apply Deployment to live cluster
        self._apply_json(dep_manifest)
        # Apply Service to live cluster
        self._apply_json(svc_manifest)
        print(f"  [ACT] Child Deployment and Service successfully applied to namespace '{namespace}'.")

    def _apply_json(self, manifest: Dict[str, Any]):
        raw = json.dumps(manifest)
        proc = subprocess.run(
            ["kubectl", "apply", "-f", "-"],
            input=raw.encode("utf-8"),
            capture_output=True,
            check=True
        )

def main():
    print("==========================================================")
    print("  WebApp Custom Controller: Educational Reconciler        ")
    print("==========================================================")

    # Mock WebApp Custom Resource
    mock_cr = {
        "apiVersion": "learning.example/v1",
        "kind": "WebApp",
        "metadata": {
            "name": "storefront",
            "namespace": "default"
        },
        "spec": {
            "image": "hashicorp/http-echo:latest",
            "replicas": 3,
            "text": "Welcome to our Storefront!",
            "port": 5678
        }
    }

    dry_run = "--live" not in sys.argv
    reconciler = WebAppReconciler(dry_run=dry_run)
    reconciler.reconcile_webapp(mock_cr)

if __name__ == "__main__":
    main()
