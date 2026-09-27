def reconcile(source_totals, warehouse_totals, tolerance=0.01):
    diff = abs(source_totals - warehouse_totals)
    return diff <= tolerance, diff
