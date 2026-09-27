"""
tests/test_simulators.py
Unit tests verifying the educational simulator engines and distributed primitives.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "projects", "project-07-tiny-cloud-simulator")))
from tiny_cloud import TinyCloud
from experiments.iam_simulator import IAMStatement, IAMPolicy, IAMEvaluator
from experiments.sqs_visibility_lab import MockSQSQueue, IdempotentPaymentConsumer
from experiments.lb_healthcheck_lab import BackendTarget, LoadBalancerTargetGroup


class TestIAMSimulator(unittest.TestCase):
    def setUp(self):
        doc = {
            "Statement": [
                {
                    "Sid": "AllowS3Read",
                    "Effect": "Allow",
                    "Action": ["s3:GetObject"],
                    "Resource": ["arn:aws:s3:::my-bucket/*"]
                },
                {
                    "Sid": "DenyS3Delete",
                    "Effect": "Deny",
                    "Action": ["s3:DeleteObject"],
                    "Resource": ["*"]
                }
            ]
        }
        self.policy = IAMPolicy.from_dict("TestPolicy", doc)
        self.evaluator = IAMEvaluator([self.policy])

    def test_explicit_allow(self):
        res = self.evaluator.evaluate("alice", "s3:GetObject", "arn:aws:s3:::my-bucket/doc.txt")
        self.assertEqual(res["decision"], "ALLOWED")
        self.assertEqual(res["reason"], "EXPLICIT_ALLOW")

    def test_explicit_deny_overrides(self):
        res = self.evaluator.evaluate("alice", "s3:DeleteObject", "arn:aws:s3:::my-bucket/doc.txt")
        self.assertEqual(res["decision"], "DENIED")
        self.assertEqual(res["reason"], "EXPLICIT_DENY")

    def test_default_deny(self):
        res = self.evaluator.evaluate("alice", "dynamodb:GetItem", "arn:aws:dynamodb:us-east-1:123:table/T")
        self.assertEqual(res["decision"], "DENIED")
        self.assertEqual(res["reason"], "DEFAULT_DENY")


class TestSQSVisibilityLab(unittest.TestCase):
    def test_visibility_and_idempotency(self):
        dlq = MockSQSQueue("dlq", visibility_timeout_sec=5.0)
        q = MockSQSQueue("primary", visibility_timeout_sec=0.2, max_receive_count=2, dlq=dlq)
        consumer = IdempotentPaymentConsumer()

        msg_id = q.send_message("ORD-100")
        msg = q.receive_message()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.body, "ORD-100")

        # Process first time
        consumer.process_message(msg)
        self.assertEqual(len(consumer.processed_bank_charges), 1)

        # Process second time (simulated duplicate delivery)
        consumer.process_message(msg)
        self.assertEqual(len(consumer.processed_bank_charges), 1, "Duplicate charge must be prevented!")


class TestLoadBalancerTargetGroup(unittest.TestCase):
    def test_health_check_eviction(self):
        tg = LoadBalancerTargetGroup("tg", healthy_threshold=2, unhealthy_threshold=2)
        inst_a = BackendTarget("i-a", "az1", "10.0.1.1", 80)
        inst_b = BackendTarget("i-b", "az2", "10.0.2.1", 80)
        tg.register_target(inst_a)
        tg.register_target(inst_b)

        # Fail instance A
        inst_a.is_alive = False
        tg.probe_health_checks()  # fail 1
        tg.probe_health_checks()  # fail 2 -> evict
        self.assertFalse(inst_a.is_healthy)

        # Forward request should go only to instance B
        resp = tg.forward_request("/test")
        self.assertIn("i-b", resp["body"])


class TestTinyCloud(unittest.TestCase):
    def test_cloud_flow(self):
        cloud = TinyCloud()
        vms = cloud.run_instances("ami-123", count=2)
        self.assertEqual(len(vms), 2)
        cloud.create_bucket("test-bucket")
        cloud.put_object("test-bucket", "hello.txt", b"hello world")
        data = cloud.get_object("test-bucket", "hello.txt")
        self.assertEqual(data, b"hello world")
        cloud.terminate_instances(vms)
        active = cloud.describe_instances(state="running")
        self.assertEqual(len(active), 0)


if __name__ == "__main__":
    unittest.main()
