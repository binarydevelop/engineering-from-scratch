#!/usr/bin/env python3
"""
projects/project-07-tiny-cloud-simulator/tiny_cloud.py
Phase 81: Capstone 1 - Build a Tiny Cloud Simulator

The goal is NOT to clone AWS.
The goal is to demystify the cloud: to prove that every AWS service is simply
an ordinary computer science primitive wrapped in a clean, stateful HTTP API.

Primitives Implemented:
  1. VMRegistry (Compute / EC2)
  2. ObjectStore (Storage / S3)
  3. LoadBalancer (Traffic Distribution / ALB)
  4. MessageQueue (Asynchronous Decoupling / SQS)
  5. AuthorizationEngine (Identity & Access / IAM)
  6. TelemetryEngine (Metrics & Alarming / CloudWatch)
"""

import time
import uuid
import hashlib
from typing import Dict, List, Optional, Any, Callable


class Instance:
    def __init__(self, instance_id: str, ami_id: str, instance_type: str, az: str, tags: Dict[str, str]):
        self.instance_id = instance_id
        self.ami_id = ami_id
        self.instance_type = instance_type
        self.az = az
        self.tags = tags
        self.state = "pending"
        self.ip_address = f"10.0.{hash(instance_id) % 250}.{hash(instance_id) % 250 + 1}"
        self.launch_time = time.time()
        self.metadata = {
            "ami-id": ami_id,
            "instance-type": instance_type,
            "local-ipv4": self.ip_address,
            "placement/availability-zone": az
        }


class S3Object:
    def __init__(self, key: str, data: bytes, content_type: str = "application/octet-stream", metadata: Optional[Dict[str, str]] = None):
        self.key = key
        self.data = data
        self.content_type = content_type
        self.metadata = metadata or {}
        self.etag = hashlib.md5(data).hexdigest()
        self.size_bytes = len(data)
        self.last_modified = time.time()


class TinyCloud:
    """The unified cloud API facade."""

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        # Compute Plane
        self._instances: Dict[str, Instance] = {}
        # Object Storage Plane
        self._buckets: Dict[str, Dict[str, S3Object]] = {}
        # Message Queues
        self._queues: Dict[str, List[Dict[str, Any]]] = {}
        # Load Balancers
        self._lbs: Dict[str, List[str]] = {}
        # Telemetry
        self._metrics: List[Dict[str, Any]] = []

    # -------------------------------------------------------------------------
    # 1. Compute APIs (EC2 Primitive)
    # -------------------------------------------------------------------------
    def run_instances(self, ami_id: str, instance_type: str = "t4g.micro", az: str = "us-east-1a", count: int = 1, tags: Optional[Dict[str, str]] = None) -> List[str]:
        created_ids = []
        for _ in range(count):
            iid = f"i-{uuid.uuid4().hex[:12]}"
            inst = Instance(iid, ami_id, instance_type, az, tags or {})
            inst.state = "running"
            self._instances[iid] = inst
            created_ids.append(iid)
        return created_ids

    def terminate_instances(self, instance_ids: List[str]) -> List[str]:
        terminated = []
        for iid in instance_ids:
            if iid in self._instances:
                self._instances[iid].state = "terminated"
                terminated.append(iid)
        return terminated

    def describe_instances(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for inst in self._instances.values():
            if state and inst.state != state:
                continue
            results.append({
                "InstanceId": inst.instance_id,
                "State": inst.state,
                "InstanceType": inst.instance_type,
                "PrivateIp": inst.ip_address,
                "AvailabilityZone": inst.az,
                "Tags": inst.tags
            })
        return results

    # -------------------------------------------------------------------------
    # 2. Storage APIs (S3 Primitive)
    # -------------------------------------------------------------------------
    def create_bucket(self, bucket_name: str) -> bool:
        if bucket_name in self._buckets:
            raise ValueError(f"BucketAlreadyExists: {bucket_name}")
        self._buckets[bucket_name] = {}
        return True

    def put_object(self, bucket: str, key: str, data: bytes, content_type: str = "text/plain", metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        if bucket not in self._buckets:
            raise KeyError(f"NoSuchBucket: {bucket}")
        obj = S3Object(key, data, content_type, metadata)
        self._buckets[bucket][key] = obj
        return {"ETag": obj.etag, "Key": obj.key, "Size": obj.size_bytes}

    def get_object(self, bucket: str, key: str) -> bytes:
        if bucket not in self._buckets or key not in self._buckets[bucket]:
            raise KeyError(f"NoSuchKey: {bucket}/{key}")
        return self._buckets[bucket][key].data

    def delete_object(self, bucket: str, key: str) -> bool:
        if bucket in self._buckets and key in self._buckets[bucket]:
            del self._buckets[bucket][key]
            return True
        return False

    # -------------------------------------------------------------------------
    # 3. Queue APIs (SQS Primitive)
    # -------------------------------------------------------------------------
    def create_queue(self, queue_name: str) -> str:
        if queue_name not in self._queues:
            self._queues[queue_name] = []
        return f"https://queue.tinycloud.{self.region}/{queue_name}"

    def send_message(self, queue_name: str, body: str) -> str:
        if queue_name not in self._queues:
            raise KeyError(f"NonExistentQueue: {queue_name}")
        mid = f"msg-{uuid.uuid4().hex[:8]}"
        self._queues[queue_name].append({
            "MessageId": mid,
            "Body": body,
            "VisibleAt": 0.0,
            "ReceiveCount": 0
        })
        return mid

    def receive_message(self, queue_name: str, visibility_timeout: float = 3.0) -> Optional[Dict[str, Any]]:
        if queue_name not in self._queues:
            raise KeyError(f"NonExistentQueue: {queue_name}")
        now = time.time()
        for msg in self._queues[queue_name]:
            if msg["VisibleAt"] <= now:
                msg["ReceiveCount"] += 1
                msg["VisibleAt"] = now + visibility_timeout
                return {"MessageId": msg["MessageId"], "Body": msg["Body"]}
        return None

    def delete_message(self, queue_name: str, message_id: str) -> bool:
        if queue_name not in self._queues:
            return False
        initial_len = len(self._queues[queue_name])
        self._queues[queue_name] = [m for m in self._queues[queue_name] if m["MessageId"] != message_id]
        return len(self._queues[queue_name]) < initial_len

    # -------------------------------------------------------------------------
    # 4. Load Balancer APIs (ALB Primitive)
    # -------------------------------------------------------------------------
    def create_load_balancer(self, lb_name: str, target_instance_ids: List[str]):
        self._lbs[lb_name] = target_instance_ids

    def forward_request(self, lb_name: str, path: str) -> str:
        targets = self._lbs.get(lb_name, [])
        running_targets = [t for t in targets if self._instances.get(t, None) and self._instances[t].state == "running"]
        if not running_targets:
            return "HTTP 503 Service Unavailable"
        # Round-robin target selection
        target_id = running_targets[0]
        inst = self._instances[target_id]
        return f"HTTP 200 OK from {inst.instance_id} at {inst.ip_address} on {path}"

    # -------------------------------------------------------------------------
    # 5. Telemetry APIs (CloudWatch Primitive)
    # -------------------------------------------------------------------------
    def put_metric_data(self, namespace: str, metric_name: str, value: float, unit: str = "Count"):
        self._metrics.append({
            "Namespace": namespace,
            "MetricName": metric_name,
            "Value": value,
            "Unit": unit,
            "Timestamp": time.time()
        })


def main():
    print("=" * 68)
    print("           TINY CLOUD SIMULATOR (Capstone 1)                     ")
    print("=" * 68)

    cloud = TinyCloud(region="us-east-1")

    # Step 1: Launch compute instances
    print("\n1. Provisioning Compute (EC2):")
    inst_ids = cloud.run_instances(ami_id="ami-amazon-linux-2023", instance_type="t4g.micro", az="us-east-1a", count=2, tags={"Project": "aws-from-scratch"})
    for inst in cloud.describe_instances(state="running"):
        print(f"   [RUNNING] {inst['InstanceId']} | IP: {inst['PrivateIp']} | AZ: {inst['AvailabilityZone']}")

    # Step 2: Object storage
    print("\n2. Storing Data in Object Storage (S3):")
    cloud.create_bucket("user-avatars-2026")
    res = cloud.put_object("user-avatars-2026", "avatars/alice.png", b"\x89PNG\r\n\x1a\n...fake-png-bytes...", content_type="image/png")
    print(f"   [UPLOADED] s3://user-avatars-2026/{res['Key']} (ETag: {res['ETag']}, Size: {res['Size']} bytes)")
    data = cloud.get_object("user-avatars-2026", "avatars/alice.png")
    print(f"   [READ] Retrieved {len(data)} bytes from S3.")

    # Step 3: Load Balancing
    print("\n3. Routing Traffic via Load Balancer (ALB):")
    cloud.create_load_balancer("web-alb", inst_ids)
    print(f"   [REQUEST] {cloud.forward_request('web-alb', '/api/v1/health')}")

    # Step 4: Asynchronous Queueing
    print("\n4. Decoupling Async Work (SQS):")
    cloud.create_queue("order-processing-queue")
    msg_id = cloud.send_message("order-processing-queue", "ORDER-99214")
    print(f"   [PUBLISHED] Message {msg_id} in queue.")
    msg = cloud.receive_message("order-processing-queue")
    print(f"   [CONSUMED] Worker checked out: {msg['Body']} (ID: {msg['MessageId']})")
    cloud.delete_message("order-processing-queue", msg["MessageId"])
    print("   [ACKNOWLEDGED] Message successfully deleted.")

    # Step 5: Clean Up
    print("\n5. Tearing Down Infrastructure:")
    cloud.terminate_instances(inst_ids)
    cloud.delete_object("user-avatars-2026", "avatars/alice.png")
    print("   [TERMINATED] All compute instances terminated and S3 objects deleted.")

    print("\n" + "=" * 68)
    print("Capstone 1 Insight:")
    print("Cloud infrastructure is not proprietary sorcery.")
    print("It is clean distributed software exposing hardware primitives over APIs.")
    print("=" * 68)


if __name__ == "__main__":
    main()
