"""
Resilient, production-ready solution for lab-26-spark-broadcast-join-oom-driver.
"""
def should_broadcast(table_size_bytes, max_broadcast_bytes=100*1024*1024):
    return table_size_bytes <= max_broadcast_bytes
