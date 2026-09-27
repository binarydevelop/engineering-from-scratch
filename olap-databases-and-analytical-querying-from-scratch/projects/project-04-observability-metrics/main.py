import duckdb
con = duckdb.connect('outputs/olap_lab.duckdb')
res = con.execute('''
    SELECT
        service_name,
        COUNT(*) as total_reqs,
        ROUND(approx_quantile(latency_ms, 0.95), 2) as p95_latency,
        ROUND(approx_quantile(latency_ms, 0.99), 2) as p99_latency,
        COUNT(CASE WHEN http_status >= 500 THEN 1 END) as error_count
    FROM service_logs
    GROUP BY service_name
''').fetchall()
print(res)
