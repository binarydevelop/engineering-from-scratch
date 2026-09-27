#!/usr/bin/env python3
"""
experiments/iam_simulator.py
Phase 03 & Phase 04: IAM From First Principles

This script implements a lightweight, first-principles authorization engine
in pure Python that mirrors AWS IAM policy evaluation semantics:
  1. Default Deny: If no statement allows, the request is Denied.
  2. Explicit Allow: An allow statement grants access.
  3. Explicit Deny Overrides All: Any matching Deny immediately terminates
     evaluation with Denied, regardless of how many Allow statements exist.
  4. Pattern Matching: Supports prefix and wildcard action/resource matching.
"""

import fnmatch
from typing import Dict, List, Any


class IAMStatement:
    def __init__(self, sid: str, effect: str, actions: List[str], resources: List[str]):
        if effect not in ("Allow", "Deny"):
            raise ValueError(f"Effect must be Allow or Deny, got: {effect}")
        self.sid = sid
        self.effect = effect
        self.actions = actions
        self.resources = resources

    def matches(self, requested_action: str, requested_resource: str) -> bool:
        action_match = any(fnmatch.fnmatch(requested_action.lower(), act.lower()) for act in self.actions)
        resource_match = any(fnmatch.fnmatch(requested_resource, res) for res in self.resources)
        return action_match and resource_match


class IAMPolicy:
    def __init__(self, name: str, statements: List[IAMStatement]):
        self.name = name
        self.statements = statements

    @classmethod
    def from_dict(cls, name: str, doc: Dict[str, Any]) -> "IAMPolicy":
        stmts = []
        for i, s in enumerate(doc.get("Statement", [])):
            sid = s.get("Sid", f"Stmt{i+1}")
            effect = s.get("Effect")
            actions = s.get("Action")
            if isinstance(actions, str):
                actions = [actions]
            resources = s.get("Resource")
            if isinstance(resources, str):
                resources = [resources]
            stmts.append(IAMStatement(sid, effect, actions, resources))
        return cls(name, stmts)


class IAMEvaluator:
    def __init__(self, policies: List[IAMPolicy]):
        self.policies = policies

    def evaluate(self, principal: str, action: str, resource: str) -> Dict[str, Any]:
        """
        Evaluates authorization using AWS precedence:
          - Step 1: Check for any matching Explicit Deny.
          - Step 2: Check for any matching Explicit Allow.
          - Step 3: Fall through to Default Deny.
        """
        matched_denies = []
        matched_allows = []

        for policy in self.policies:
            for stmt in policy.statements:
                if stmt.matches(action, resource):
                    if stmt.effect == "Deny":
                        matched_denies.append((policy.name, stmt.sid))
                    elif stmt.effect == "Allow":
                        matched_allows.append((policy.name, stmt.sid))

        if matched_denies:
            return {
                "decision": "DENIED",
                "reason": "EXPLICIT_DENY",
                "details": f"Request explicitly denied by statement: {matched_denies[0]}",
                "principal": principal,
                "action": action,
                "resource": resource
            }

        if matched_allows:
            return {
                "decision": "ALLOWED",
                "reason": "EXPLICIT_ALLOW",
                "details": f"Request allowed by statement: {matched_allows[0]}",
                "principal": principal,
                "action": action,
                "resource": resource
            }

        return {
            "decision": "DENIED",
            "reason": "DEFAULT_DENY",
            "details": "No policy statement granted an explicit Allow.",
            "principal": principal,
            "action": action,
            "resource": resource
        }


def run_interactive_demo():
    print("=" * 65)
    print("      IAM Policy Evaluation From First Principles Simulator      ")
    print("=" * 65)

    # Define Policy 1: Developer Access (Allows S3 Read/Write in lab bucket)
    dev_policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowLabS3ReadWrite",
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:PutObject"],
                "Resource": ["arn:aws:s3:::aws-from-scratch-lab/*"]
            },
            {
                "Sid": "AllowDynamoDBReads",
                "Effect": "Allow",
                "Action": ["dynamodb:GetItem", "dynamodb:Query"],
                "Resource": ["arn:aws:dynamodb:*:*:table/Orders"]
            }
        ]
    }

    # Define Policy 2: Security Guardrail / SCP (Explicit Deny on deleting objects or prod buckets)
    guardrail_policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DenyProductionBucketAccess",
                "Effect": "Deny",
                "Action": ["s3:*"],
                "Resource": ["arn:aws:s3:::production-data-*/*"]
            },
            {
                "Sid": "DenyObjectDeletion",
                "Effect": "Deny",
                "Action": ["s3:DeleteObject*"],
                "Resource": ["*"]
            }
        ]
    }

    dev_policy = IAMPolicy.from_dict("DeveloperAccessPolicy", dev_policy_doc)
    guardrail_policy = IAMPolicy.from_dict("SecurityGuardrailPolicy", guardrail_policy_doc)

    evaluator = IAMEvaluator([dev_policy, guardrail_policy])

    scenarios = [
        (
            "Scenario 1: Read object from lab bucket (Expect ALLOW)",
            "alice",
            "s3:GetObject",
            "arn:aws:s3:::aws-from-scratch-lab/report.pdf"
        ),
        (
            "Scenario 2: Delete object from lab bucket (Expect DENY via Default Deny)",
            "alice",
            "s3:DeleteObject",
            "arn:aws:s3:::aws-from-scratch-lab/report.pdf"
        ),
        (
            "Scenario 3: Read from production bucket (Expect DENY via Explicit Deny)",
            "alice",
            "s3:GetObject",
            "arn:aws:s3:::production-data-vault/secrets.json"
        ),
        (
            "Scenario 4: Query DynamoDB Orders table (Expect ALLOW)",
            "alice",
            "dynamodb:Query",
            "arn:aws:dynamodb:us-east-1:123456789012:table/Orders"
        ),
        (
            "Scenario 5: Describe EC2 instances (Expect DENY via Default Deny)",
            "alice",
            "ec2:DescribeInstances",
            "*"
        )
    ]

    for title, principal, action, resource in scenarios:
        print(f"\n{title}")
        print(f"  Principal: {principal} | Action: {action} | Resource: {resource}")
        result = evaluator.evaluate(principal, action, resource)
        decision_color = "\033[92m" if result["decision"] == "ALLOWED" else "\033[91m"
        reset_color = "\033[0m"
        print(f"  Result:   {decision_color}{result['decision']}{reset_color} ({result['reason']})")
        print(f"  Details:  {result['details']}")

    print("\n" + "=" * 65)
    print("First-Principles Realization:")
    print("AWS IAM is not a black box: it is a deterministic boolean reduction")
    print("engine where Explicit Deny > Explicit Allow > Default Deny.")
    print("=" * 65)


if __name__ == "__main__":
    run_interactive_demo()
