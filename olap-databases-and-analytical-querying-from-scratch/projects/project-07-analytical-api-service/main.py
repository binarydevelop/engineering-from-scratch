# Analytical Query Service with Concurrency Control
import duckdb
import time

def serve_analytical_query(tenant_id: int, timeout_sec: float = 3.0):
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.time()
    try:
        res = con.execute('SELECT country, SUM(net_revenue) FROM fact_order_items GROUP BY country').fetchall()
        elapsed = time.time() - t0
        return {'status': 'success', 'elapsed_s': elapsed, 'data': res}
    finally:
        con.close()

if __name__ == '__main__':
    print(serve_analytical_query(42))
