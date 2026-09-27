#!/usr/bin/env python3

def calculate_pointer_waste(num_objects=500_000_000):
    # Compressed OOPs (<= 31GB): 4 bytes per pointer
    compressed_bytes = num_objects * 4
    # Uncompressed OOPs (> 32GB): 8 bytes per pointer
    uncompressed_bytes = num_objects * 8
    wasted_gb = (uncompressed_bytes - compressed_bytes) / (1024 ** 3)
    return wasted_gb

if __name__ == "__main__":
    waste = calculate_pointer_waste(500_000_000)
    print("Compressed OOPs (Ordinary Object Pointers) Analysis:")
    print(f"For 500 million Java heap objects, crossing 32GB wastes {waste:.2f} GB of RAM purely on 64-bit pointer padding!")
    print("Always cap Elasticsearch JVM Heap at 31 GB!")
