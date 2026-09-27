import duckdb

def build_star_schema(con):
    con.execute("""
        CREATE TABLE dim_cust (cust_sk INT PRIMARY KEY, user_id VARCHAR, tier VARCHAR);
        CREATE TABLE fact_ord (order_id VARCHAR PRIMARY KEY, cust_sk INT, amount NUMERIC(10,2));
        INSERT INTO dim_cust VALUES (1, 'u1', 'VIP'), (2, 'u2', 'STANDARD');
        INSERT INTO fact_ord VALUES ('o1', 1, 150.0), ('o2', 2, 50.0);
    """)
    res = con.execute("""
        SELECT d.tier, SUM(f.amount) as revenue
        FROM fact_ord f JOIN dim_cust d ON f.cust_sk = d.cust_sk
        GROUP BY d.tier ORDER BY revenue DESC;
    """).fetchall()
    return res
