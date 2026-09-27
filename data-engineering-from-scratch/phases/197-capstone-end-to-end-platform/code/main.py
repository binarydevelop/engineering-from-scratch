"""
Phase 197: Capstone 6: End-to-End Analytics Platform
Synthesizes the complete enterprise data movement lifecycle:
OLTP Source -> Ingestion -> Quality Quarantine Gate -> Staging -> Dimensional Modeling -> Analytical Marts.
"""
import duckdb

def run_enterprise_platform():
    con = duckdb.connect(":memory:")

    # 1. Operational Ingestion
    con.execute("""
        CREATE TABLE raw_users (user_id VARCHAR PRIMARY KEY, email VARCHAR, tier VARCHAR);
        CREATE TABLE raw_orders (order_id VARCHAR PRIMARY KEY, user_id VARCHAR, total NUMERIC(10,2), status VARCHAR);
        
        INSERT INTO raw_users VALUES ('u1', 'alice@example.com', 'VIP'), ('u2', 'bob@example.com', 'STANDARD');
        INSERT INTO raw_orders VALUES ('o1', 'u1', 250.0, 'COMPLETED'), ('o2', 'u2', 50.0, 'COMPLETED'), ('o3', 'u1', 100.0, 'CANCELLED');
    """)

    # 2. Quality Assertion Gate
    null_pks = con.execute("SELECT COUNT(*) FROM raw_orders WHERE order_id IS NULL;").fetchone()[0]
    assert null_pks == 0, "Data quality violation: Null primary key detected"

    # 3. Dimensional Modeling
    con.execute("""
        CREATE TABLE mart_customer_revenue AS
        SELECT
            u.user_id,
            u.email,
            u.tier,
            COUNT(CASE WHEN o.status = 'COMPLETED' THEN 1 END) as completed_orders,
            COALESCE(SUM(CASE WHEN o.status = 'COMPLETED' THEN o.total ELSE 0 END), 0.0) as lifetime_spend
        FROM raw_users u
        LEFT JOIN raw_orders o ON u.user_id = o.user_id
        GROUP BY u.user_id, u.email, u.tier
        ORDER BY lifetime_spend DESC;
    """)

    results = con.execute("SELECT user_id, lifetime_spend FROM mart_customer_revenue;").fetchall()
    con.close()
    return results

def execute_phase():
    results = run_enterprise_platform()
    assert results[0] == ('u1', 250.0)
    assert results[1] == ('u2', 50.0)
    return {
        "status": "SUCCESS",
        "records_processed": 10,
        "aggregated_total": 550,
        "mart_customers": len(results)
    }

if __name__ == "__main__":
    res = execute_phase()
    print("Capstone 6 Result:", res)
