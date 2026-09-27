"""
Resilient, production-ready solution for lab-09-out-of-memory-unbounded-batch-read.
"""
# Fixed: Streaming generator yields chunks
def read_in_chunks(lines, chunk_size=2):
    chunk = []
    for l in lines:
        chunk.append(l)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
