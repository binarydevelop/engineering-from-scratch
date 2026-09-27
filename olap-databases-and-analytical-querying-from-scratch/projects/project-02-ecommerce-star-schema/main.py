import duckdb
con = duckdb.connect('outputs/olap_lab.duckdb')
res = con.execute('''
    SELECT u.acquisition_channel, COUNT(DISTINCT f.user_id) as users, ROUND(SUM(f.net_revenue), 2) as rev
    FROM fact_order_items f
    JOIN dim_users u ON f.user_id = u.user_id
    GROUP BY u.acquisition_channel
    ORDER BY rev DESC
''').fetchall()
print(res)
