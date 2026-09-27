#!/usr/bin/env python3
"""
GitOps Reconciler Engine (Phases 153-165, 203, 204, 215)
Implements GitOps reconciliation loop:
- Watches desired state declared in Git configuration directory
- Inspects actual running cluster state
- Detects drift between desired and live state
- Reconciles live state toward Git desired state
- Safeguards against dangerous destructive sync options
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, Any, Tuple


class GitOpsReconciler:
    def __init__(self, desired_dir: str, live_dir: str):
        self.desired_dir = desired_dir
        self.live_dir = live_dir
        os.makedirs(self.desired_dir, exist_ok=True)
        os.makedirs(self.live_dir, exist_ok=True)
        self._seed_default_state()

    def _seed_default_state(self):
        desired_file = os.path.join(self.desired_dir, "delivery-service.json")
        live_file = os.path.join(self.live_dir, "delivery-service.json")

        if not os.path.exists(desired_file):
            default_spec = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {"name": "delivery-service", "namespace": "production"},
                "spec": {
                    "replicas": 3,
                    "image": "ghcr.io/binarydevelop/delivery-service:1.0.0",
                    "digest": "sha256:7041b28e74403e789f88bbf6cc2474c8fd7995b283c62819f80b4165b0fb47f0",
                    "env": {"ENVIRONMENT": "production"}
                }
            }
            with open(desired_file, "w") as f:
                json.dump(default_spec, f, indent=2)

        if not os.path.exists(live_file):
            # Initially in sync
            with open(desired_file, "r") as df, open(live_file, "w") as lf:
                lf.write(df.read())

    def get_desired_state(self) -> Dict[str, Any]:
        with open(os.path.join(self.desired_dir, "delivery-service.json"), "r") as f:
            return json.load(f)

    def get_live_state(self) -> Dict[str, Any]:
        with open(os.path.join(self.live_dir, "delivery-service.json"), "r") as f:
            return json.load(f)

    def detect_drift(self) -> Tuple[bool, Dict[str, Any]]:
        desired = self.get_desired_state()
        live = self.get_live_state()

        diffs = {}
        # Compare key fields
        if desired["spec"]["image"] != live["spec"]["image"]:
            diffs["image"] = {"desired": desired["spec"]["image"], "live": live["spec"]["image"]}
        if desired["spec"]["digest"] != live["spec"]["digest"]:
            diffs["digest"] = {"desired": desired["spec"]["digest"], "live": live["spec"]["digest"]}
        if desired["spec"]["replicas"] != live["spec"]["replicas"]:
            diffs["replicas"] = {"desired": desired["spec"]["replicas"], "live": live["spec"]["replicas"]}

        is_drifted = len(diffs) > 0
        return is_drifted, diffs

    def sync(self, dry_run: bool = False, force_replace: bool = False) -> bool:
        is_drifted, diffs = self.detect_drift()
        print("=== GITOPS RECONCILER STATUS ===")
        print(f"Desired State Source: {self.desired_dir}/delivery-service.json")
        print(f"Live Cluster Target : {self.live_dir}/delivery-service.json")

        if not is_drifted:
            print("\n✓ Cluster Status: [Synced] — Desired state matches live state.")
            return True

        print("\n⚠ Cluster Status: [OutOfSync] — Drift detected!")
        for field, detail in diffs.items():
            print(f"  - Field '{field}': Desired=[{detail['desired']}] vs Live=[{detail['live']}]")

        if force_replace:
            print("\n[CAUTION] --replace / --force flag enabled!")
            print("Current Argo CD documentation warns that force-replace deletes existing live pods,")
            print("causing sudden downtime and dropping ongoing customer requests!")

        if dry_run:
            print("\n[DRY RUN] No changes applied to live cluster state.")
            return False

        print("\n[RECONCILING] Synchronizing live cluster toward desired Git specification...")
        time.sleep(0.1)
        desired = self.get_desired_state()
        with open(os.path.join(self.live_dir, "delivery-service.json"), "w") as f:
            json.dump(desired, f, indent=2)

        print("✓ Reconciliation complete. Cluster status transitioned: [OutOfSync] -> [Synced].")
        return True

    def inject_manual_drift(self, tampered_replicas: int):
        """Simulates an engineer manually running 'kubectl scale' or 'kubectl edit' behind Git's back."""
        print(f"\n[SIMULATION] Engineer manually ran 'kubectl scale --replicas={tampered_replicas}' on live cluster...")
        live = self.get_live_state()
        live["spec"]["replicas"] = tampered_replicas
        with open(os.path.join(self.live_dir, "delivery-service.json"), "w") as f:
            json.dump(live, f, indent=2)
        print("Live cluster mutated out-of-band.")


def main():
    parser = argparse.ArgumentParser(description="GitOps Reconciler Simulator")
    parser.add_argument("--mode", choices=["status", "sync", "dry-run", "simulate-drift"], default="status")
    parser.add_argument("--desired-dir", default=os.path.join(os.path.dirname(__file__), "desired-state"))
    parser.add_argument("--live-dir", default=os.path.join(os.path.dirname(__file__), "live-cluster"))
    parser.add_argument("--force-replace", action="store_true", help="Demonstrate dangerous force-replace option")
    args = parser.parse_args()

    reconciler = GitOpsReconciler(args.desired_dir, args.live_dir)

    if args.mode == "status":
        drifted, _ = reconciler.detect_drift()
        reconciler.sync(dry_run=True)
    elif args.mode == "dry-run":
        reconciler.sync(dry_run=True)
    elif args.mode == "sync":
        reconciler.sync(dry_run=False, force_replace=args.force_replace)
    elif args.mode == "simulate-drift":
        reconciler.inject_manual_drift(tampered_replicas=10)
        reconciler.sync(dry_run=True)


if __name__ == "__main__":
    main()
