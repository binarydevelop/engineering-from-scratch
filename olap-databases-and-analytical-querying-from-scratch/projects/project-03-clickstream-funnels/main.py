import duckdb
con = duckdb.connect('outputs/olap_lab.duckdb')
res = con.execute('''
    SELECT
        COUNT(DISTINCT user_id) as total_visitors,
        COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) as step_view,
        COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) as step_cart,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) as step_purchase
    FROM web_events
''').fetchall()
print(res)
