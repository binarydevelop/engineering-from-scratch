"""
Resilient, production-ready solution for lab-21-lineage-graph-broken-dependency-gap.
"""
# Fixed: Explicit DAG dependency lineage registry
def record_lineage(registry, upstream, downstream):
    registry.setdefault(downstream, set()).add(upstream)
