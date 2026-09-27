#!/usr/bin/env python3
"""
Platform CLI (`platform-cli`): Developer self-service and production readiness tooling.
Implemented using standard library primitives so it runs without external dependencies.
"""

import os
import sys
import argparse
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scorecards.evaluator import evaluate_service_directory


def parse_simple_yaml(filepath: str) -> Dict[str, Any]:
    """Lightweight YAML parser for simple key-value and list structures."""
    try:
        import yaml
        with open(filepath, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except ImportError:
        # Fallback minimal parser if pyyaml not installed
        data: Dict[str, Any] = {"services": []}
        current_service: Dict[str, Any] = {}
        with open(filepath, "r", encoding="utf-8") as fh:
            for line in fh:
                line_str = line.strip()
                if line_str.startswith("- name:"):
                    if current_service:
                        data["services"].append(current_service)
                    current_service = {"name": line_str.split(":", 1)[1].strip()}
                elif current_service and ":" in line_str:
                    k, v = line_str.split(":", 1)
                    k = k.strip().lstrip("- ")
                    v = v.strip().strip('"').strip("'")
                    current_service[k] = v
        if current_service:
            data["services"].append(current_service)
        return data


def new_service(name: str, team: str, port: int, output_dir: str):
    """Scaffolds a production-ready observable microservice from the Golden Path template."""
    target_dir = os.path.join(output_dir, name)
    if os.path.exists(target_dir):
        print(f"[ERROR] Target directory already exists: {target_dir}", file=sys.stderr)
        sys.exit(1)

    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates", "service_template")
    os.makedirs(target_dir, exist_ok=True)

    # Copy files and replace template variables
    for item in os.listdir(template_dir):
        s = os.path.join(template_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isfile(s):
            with open(s, "r", encoding="utf-8") as fh:
                content = fh.read()
            content = content.replace("{{service_name}}", name)
            content = content.replace("{{team_name}}", team)
            content = content.replace("{{port}}", str(port))
            with open(d, "w", encoding="utf-8") as fh:
                fh.write(content)

    print(f"[SUCCESS] Scaffolding complete for service '{name}' in {target_dir}")
    print(f"  - Health endpoints:  /healthz, /ready")
    print(f"  - Metrics endpoint:  /metrics")
    print(f"  - Declarative spec:  service.yaml")
    print(f"  - Dockerfile:        Dockerfile")
    print(f"Run 'python3 platform/cli/main.py scorecard --dir {target_dir}' to verify production readiness.")


def scorecard(service_dir: str):
    """Audits a service against the Production Readiness Review (PRR) checklist."""
    results = evaluate_service_directory(service_dir)
    if "error" in results:
        print(f"[ERROR] {results['error']}", file=sys.stderr)
        sys.exit(1)

    print("=========================================================================")
    print(f"       PRODUCTION READINESS SCORECARD: {os.path.basename(service_dir)}   ")
    print("=========================================================================")
    print(f" Grade:            {results['grade']}")
    print(f" Compliance Score: {results['score_percent']:.1f}% ({results['passed_count']}/{results['total_checks']} invariants met)")
    print("-------------------------------------------------------------------------")
    for detail in results["details"]:
        print(f"  {detail}")
    print("=========================================================================")


def catalog(catalog_file: str):
    """Displays the declarative software catalog and dependency topology."""
    if not os.path.exists(catalog_file):
        print(f"[ERROR] Catalog file not found: {catalog_file}", file=sys.stderr)
        sys.exit(1)

    data = parse_simple_yaml(catalog_file)
    services = data.get("services", [])
    print("=========================================================================")
    print("                       INTERNAL SOFTWARE CATALOG                         ")
    print("=========================================================================")
    print(f"{'Service Name':<22} {'Team':<18} {'Tier':<8} {'Port':<6} {'Dependencies'}")
    print("-------------------------------------------------------------------------")
    for s in services:
        deps = s.get("dependencies", "None")
        if isinstance(deps, list):
            deps = ", ".join(deps)
        print(f"{s.get('name', 'unknown'):<22} {s.get('team', 'unknown'):<18} {s.get('tier', 'tier-1'):<8} {str(s.get('port', 'N/A')):<6} {deps}")
    print("=========================================================================")


def generate_manifests(service_file: str):
    """Translates developer service.yaml into Kubernetes Deployment & Service manifests."""
    if not os.path.exists(service_file):
        print(f"[ERROR] File not found: {service_file}", file=sys.stderr)
        sys.exit(1)

    with open(service_file, "r", encoding="utf-8") as fh:
        raw_text = fh.read()

    name = "service"
    port = 8080
    for line in raw_text.splitlines():
        if "name:" in line and "metadata" not in line:
            name = line.split(":", 1)[1].strip()
        if "port:" in line:
            try:
                port = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass

    k8s_yaml = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
  labels:
    app: {name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
        - name: {name}
          image: internal.registry/{name}:latest
          ports:
            - containerPort: {port}
          resources:
            limits:
              cpu: "500m"
              memory: "512Mi"
            requests:
              cpu: "100m"
              memory: "128Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: {port}
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: {port}
            initialDelaySeconds: 2
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: {name}
spec:
  type: ClusterIP
  ports:
    - port: {port}
      targetPort: {port}
  selector:
    app: {name}
"""
    print(k8s_yaml)


def main():
    parser = argparse.ArgumentParser(description="Platform Engineering CLI: Golden Paths, Scorecards & Service Scaffolding")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # new-service
    p_new = subparsers.add_parser("new-service", help="Scaffold a new microservice from Golden Path template")
    p_new.add_argument("--name", required=True, help="Service name")
    p_new.add_argument("--team", required=True, help="Owning team name")
    p_new.add_argument("--port", type=int, default=8080, help="Port")
    p_new.add_argument("--output-dir", default="services", help="Destination folder")

    # scorecard
    p_score = subparsers.add_parser("scorecard", help="Audit service production readiness")
    p_score.add_argument("--dir", required=True, help="Path to service directory")

    # catalog
    p_cat = subparsers.add_parser("catalog", help="Display software catalog")
    p_cat.add_argument("--catalog-file", default="platform/catalog/services.yaml", help="Path to catalog")

    # generate-manifests
    p_gen = subparsers.add_parser("generate-manifests", help="Generate Kubernetes manifests from service.yaml")
    p_gen.add_argument("--service-file", required=True, help="Path to service.yaml")

    args = parser.parse_args()

    if args.command == "new-service":
        new_service(args.name, args.team, args.port, args.output_dir)
    elif args.command == "scorecard":
        scorecard(args.dir)
    elif args.command == "catalog":
        catalog(args.catalog_file)
    elif args.command == "generate-manifests":
        generate_manifests(args.service_file)


if __name__ == "__main__":
    main()
