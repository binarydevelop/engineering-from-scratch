import duckdb
from pathlib import Path

def run_pipeline(orders_csv, output_db):
    con = duckdb.connect(str(output_db))
    con.execute(f"""
        CREATE OR REPLACE TABLE stg_orders AS
        SELECT order_id, user_id, CAST(total_amount AS NUMERIC(10,2)) as amount, created_at
        FROM read_csv_auto('{orders_csv}')
        WHERE order_id IS NOT NULL;
    """)
    con.execute("""
        CREATE OR REPLACE TABLE fact_sales AS
        SELECT
            order_id,
            user_id,
            amount,
            strftime(CAST(created_at AS TIMESTAMP), '%Y%m%d')::INT as date_key
        FROM stg_orders;
    """)
    count = con.execute("SELECT COUNT(*) FROM fact_sales;").fetchone()[0]
    con.close()
    return count
