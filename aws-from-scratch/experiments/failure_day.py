#!/usr/bin/env python3
"""
experiments/failure_day.py
Phase 83: Failure Day - Controlled Systems Chaos & Disaster Recovery

"Everything fails, all the time." — Werner Vogels

This script provides a reproducible chaos testing harness. It walks learners through
the 7 fundamental failure modes of cloud systems:
  1. Compute Node Termination (Kill instance / container)
  2. IAM Permission Revocation (Sudden AccessDenied)
  3. Security Group Severing (Silent packet drop / timeout)
  4. Asynchronous Consumer Stall (Queue backup / poison pill)
  5. Target Group Health Check Failure (Cascading 502/503 errors)
  6. Subnet Routing Table Misconfiguration (Missing 0.0.0.0/0 route)
  7. Transient Cache Loss (Cache stampede / database spike)

For each failure:
  Predict ──► Break ──► Observe ──► Diagnose ──► Recover ──► Explain
"""

import sys
import time
from typing import Dict, Any


def run_scenario(number: int, name: str, scenario_data: Dict[str, Any]):
    print("\n" + "=" * 70)
    print(f"  SCENARIO {number}: {name.upper()}")
    print("=" * 70)

    print(f"\n[1. PREDICT]")
    print(f"  Question: {scenario_data['predict_question']}")
    print(f"  Expected Symptom: {scenario_data['expected_symptom']}")

    print(f"\n[2. BREAK]")
    print(f"  Simulating Failure: {scenario_data['break_action']}")
    time.sleep(0.3)

    print(f"\n[3. OBSERVE]")
    print(f"  System Telemetry / Error Output:")
    for line in scenario_data['error_log']:
        print(f"    | {line}")

    print(f"\n[4. DIAGNOSE]")
    print(f"  Diagnostic Tree:")
    for step in scenario_data['diagnostic_steps']:
        print(f"    ✓ {step}")

    print(f"\n[5. RECOVER]")
    print(f"  Recovery Action: {scenario_data['recovery_action']}")
    print(f"  Verification:    {scenario_data['verification']}")

    print(f"\n[6. FIRST-PRINCIPLES EXPLANATION]")
    print(f"  Why this happened: {scenario_data['explanation']}")


def main():
    print("=" * 70)
    print("                 PHASE 83: FAILURE DAY RUNNER                         ")
    print("      'Understand it. Break it. Diagnose it. Recover it.'            ")
    print("=" * 70)

    scenarios = [
        (
            1,
            "Compute Process Outage",
            {
                "predict_question": "What happens when an EC2 worker process crashes while an ALB is routing traffic?",
                "expected_symptom": "ALB returns 502 Bad Gateway until health checks fail, then traffic shifts to surviving instance.",
                "break_action": "Killed application daemon PID 4102 on i-0192a (TCP RST sent on connect).",
                "error_log": [
                    "HTTP/1.1 502 Bad Gateway",
                    "x-amzn-errortype: Target.FailedHTTPResponse",
                    "CloudWatch: TargetResponseTime p99 jumped to 15,000ms"
                ],
                "diagnostic_steps": [
                    "Check ALB target group health: instance i-0192a transitioning to UNHEALTHY.",
                    "SSH / SSM session into instance: systemctl status myapp shows 'dead (code=killed)'."
                ],
                "recovery_action": "Systemd auto-restart unit triggered; or ASG replaces terminated instance.",
                "verification": "ALB Target Group reports 2/2 targets HEALTHY; HTTP 200 OK restored.",
                "explanation": "ALBs do not instantly know an instance died until the next health check probe. Retries on 502 or cross-zone load balancing softens the impact."
            }
        ),
        (
            2,
            "IAM Permission Revocation",
            {
                "predict_question": "What happens when someone edits the EC2 Instance Profile to remove s3:GetObject?",
                "expected_symptom": "Application receives immediate HTTP 403 Forbidden with AccessDenied.",
                "break_action": "Detached policy 'AmazonS3ReadOnlyAccess' from role 'EC2-App-Role'.",
                "error_log": [
                    "botocore.exceptions.ClientError: An error occurred (AccessDenied)",
                    "when calling the GetObject operation: Access Denied",
                    "HTTP Status: 403 Forbidden"
                ],
                "diagnostic_steps": [
                    "Check sts:get-caller-identity inside application: confirms role EC2-App-Role.",
                    "Query IAM Policy Simulator: confirms s3:GetObject is evaluated as DEFAULT_DENY."
                ],
                "recovery_action": "Reattach least-privilege IAM policy granting s3:GetObject to bucket ARN.",
                "verification": "boto3 s3.get_object() succeeds immediately without instance reboot.",
                "explanation": "IAM policies are evaluated dynamically on every AWS API request. Changes take effect within seconds; no server restart is needed."
            }
        ),
        (
            3,
            "Security Group Misconfiguration",
            {
                "predict_question": "What happens when inbound port 5432 (PostgreSQL) is removed from the DB Security Group?",
                "expected_symptom": "Application server database connections hang and time out (SYN packet dropped).",
                "break_action": "Removed rule 'Inbound TCP 5432 from App-SG' in db-security-group.",
                "error_log": [
                    "psycopg2.OperationalError: could not connect to server: Connection timed out",
                    "Is the server running on host 'db.rds.amazonaws.com' and accepting TCP/IP connections?",
                    "Packet capture (tcpdump): Outgoing SYN sent, zero ACK received (silent drop)."
                ],
                "diagnostic_steps": [
                    "Observe 'timed out' (NOT 'connection refused') -> implies packet firewall drop!",
                    "Inspect RDS Security Group inbound rules: confirms TCP 5432 is missing."
                ],
                "recovery_action": "Add inbound rule: TCP 5432 from App-SG security group ID.",
                "verification": "psycopg2 connection establishes within 2 milliseconds.",
                "explanation": "Security Groups are stateful hypervisor packet filters. Disallowed packets are discarded silently without ICMP unreachable messages."
            }
        ),
        (
            4,
            "Queue Consumer Poison Pill",
            {
                "predict_question": "What happens when a malformed JSON payload enters an SQS queue without a DLQ?",
                "expected_symptom": "Queue consumer crashes, message visibility expires, message reappears, consumer crashes again forever.",
                "break_action": "Sent invalid binary byte sequence to standard SQS queue.",
                "error_log": [
                    "json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
                    "CloudWatch Metric: ApproximateNumberOfMessagesVisible oscillates between 0 and 1.",
                    "CloudWatch Metric: ApproximateNumberOfMessagesNotVisible oscillates between 1 and 0."
                ],
                "diagnostic_steps": [
                    "Check SQS ApproximateReceiveCount metric: value is > 200!",
                    "Realize message is stuck in an infinite retry loop."
                ],
                "recovery_action": "Attach a Dead-Letter Queue (DLQ) with maxReceiveCount=3.",
                "verification": "After 3 failed attempts, SQS routes poison message to DLQ; primary queue clears.",
                "explanation": "At-least-once distributed queues require dead-letter queues to catch unprocessable inputs, preventing head-of-line blocking."
            }
        ),
        (
            5,
            "Subnet Routing Table Black Hole",
            {
                "predict_question": "What happens if someone deletes the 0.0.0.0/0 -> igw-xxxx route in a public subnet?",
                "expected_symptom": "Instances in that subnet lose all internet access immediately. Inbound public traffic fails.",
                "break_action": "Deleted default route 0.0.0.0/0 from Route Table rtb-pub-subnet-1.",
                "error_log": [
                    "curl: (7) Failed to connect to api.github.com: Network is unreachable",
                    "traceroute: Destination host unreachable at first hop"
                ],
                "diagnostic_steps": [
                    "Run 'aws ec2 describe-route-tables --route-table-ids rtb-pub-subnet-1'.",
                    "Notice only the 10.0.0.0/16 'local' route remains!"
                ],
                "recovery_action": "Execute: aws ec2 create-route --route-table-id rtb-pub-subnet-1 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-xxxx.",
                "verification": "curl -I https://aws.amazon.com returns HTTP 200 within 20ms.",
                "explanation": "Without a default route targeting an Internet Gateway, the VPC virtual router drops all egress packets destined outside 10.0.0.0/16."
            }
        )
    ]

    for num, name, data in scenarios:
        run_scenario(num, name, data)

    print("\n" + "=" * 70)
    print("                      FAILURE DAY COMPLETE                            ")
    print("  You no longer fear failures: you understand their physical cause.   ")
    print("=" * 70)


if __name__ == "__main__":
    main()
