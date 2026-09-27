import duckdb
con = duckdb.connect()
res = con.execute('''
    SELECT country, COUNT(*) as cnt, ROUND(SUM(net_revenue), 2) as rev
    FROM read_parquet('datasets/ecommerce/fact_order_items.parquet')
    WHERE created_at >= '2025-01-01'
    GROUP BY country
    ORDER BY rev DESC
''').fetchall()
print(res)
