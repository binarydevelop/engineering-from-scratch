#!/usr/bin/env python3
import time
import random

def service_inventory(order_id):
    time.sleep(0.010) # 10ms
    return "inventory_reserved"

def service_payment(order_id):
    time.sleep(0.030) # 30ms
    return "payment_processed"

def service_analytics(order_id, slow=False):
    if slow:
        time.sleep(0.400) # 400ms latency spike
    else:
        time.sleep(0.005)
    return "analytics_recorded"

def service_email(order_id, failing=False):
    if failing:
        time.sleep(1.0) # 1s timeout
        raise TimeoutError("Email gateway timeout!")
    time.sleep(0.015)
    return "email_sent"

def synchronous_checkout(order_id, slow_analytics=False, fail_email=False):
    start = time.time()
    results = {}
    try:
        results['inventory'] = service_inventory(order_id)
        results['payment'] = service_payment(order_id)
        results['analytics'] = service_analytics(order_id, slow=slow_analytics)
        results['email'] = service_email(order_id, failing=fail_email)
        duration_ms = (time.time() - start) * 1000
        print(f"Checkout {order_id} SUCCEEDED in {duration_ms:.1f}ms")
        return True, duration_ms
    except Exception as e:
        duration_ms = (time.time() - start) * 1000
        print(f"Checkout {order_id} FAILED after {duration_ms:.1f}ms with error: {e}")
        return False, duration_ms

if __name__ == "__main__":
    print("--- 1. Normal Conditions ---")
    synchronous_checkout("ORD-101")

    print("\n--- 2. Slow Downstream Analytics ---")
    synchronous_checkout("ORD-102", slow_analytics=True)

    print("\n--- 3. Downstream Email Failure (Cascading Outage) ---")
    synchronous_checkout("ORD-103", fail_email=True)
