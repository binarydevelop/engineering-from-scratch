#!/usr/bin/env python3
import subprocess
import time

def test_follower_failure():
    print("=== Chaos Scenario 1: Stopping Follower Broker (kafka-node-3) ===")
    subprocess.run(["docker", "stop", "kafka-node-3"], check=False)
    print("kafka-node-3 stopped. Waiting 5s...")
    time.sleep(5)
    print("Restarting kafka-node-3...")
    subprocess.run(["docker", "start", "kafka-node-3"], check=False)
    print("kafka-node-3 restored! Check ISR recovery.")

if __name__ == "__main__":
    test_follower_failure()
