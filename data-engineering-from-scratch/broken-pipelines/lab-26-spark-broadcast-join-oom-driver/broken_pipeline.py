"""
Broken implementation demonstrating the flaw in lab-26-spark-broadcast-join-oom-driver.
"""
def should_broadcast(table_size_bytes):
    return True # Broadcasts regardless of size
