#!/usr/bin/env python3
"""
PostgreSQL Connection Pool Exhaustion Tool.

Opens concurrent database sessions and holds them idle in transaction
to demonstrate connection pool starvation and upstream queue collapse.
"""

import argparse
import time
import sys

try:
    import psycopg2
except ImportError:
    psycopg2 = None


def exhaust_pool(host: str, port: int, db: str, user: str, password: str, num_conns: int, hold_sec: int):
    if psycopg2 is None:
        print("[WARN] psycopg2 is not installed. To run real DB saturation against PostgreSQL:")
        print("  pip install psycopg2-binary")
        return

    print("=========================================================================")
    print(f" [CHAOS] Opening {num_conns} concurrent connections to {host}:{port}/{db}")
    print(f" Holding connections idle for {hold_sec} seconds...")
    print("=========================================================================")

    connections = []
    try:
        for i in range(num_conns):
            conn = psycopg2.connect(host=host, port=port, dbname=db, user=user, password=password)
            cursor = conn.cursor()
            cursor.execute("BEGIN; SELECT pg_backend_pid();")
            connections.append(conn)
            if (i + 1) % 10 == 0 or (i + 1) == num_conns:
                print(f"  -> Opened {i + 1}/{num_conns} connections")

        print("[CHAOS] Pool exhaustion active. Upstream requests should now wait or timeout.")
        time.sleep(hold_sec)
    except Exception as e:
        print(f"[CHAOS RESULT] Pool saturated or error: {e}")
    finally:
        print("Closing connections and releasing slots...")
        for c in connections:
            try:
                c.rollback()
                c.close()
            except Exception:
                pass
        print("[SAFETY] All chaos connections released.")


def main():
    parser = argparse.ArgumentParser(description="Database Connection Pool Exhaustion Harness")
    parser.add_argument("--host", type=str, default="localhost", help="PostgreSQL host")
    parser.add_argument("--port", type=int, default=5432, help="PostgreSQL port")
    parser.add_argument("--db", type=str, default="production_store", help="Database name")
    parser.add_argument("--user", type=str, default="sre_admin", help="Database user")
    parser.add_argument("--password", type=str, default="reliable_production_secret_2026", help="Password")
    parser.add_argument("--connections", type=int, default=55, help="Number of connections to acquire")
    parser.add_argument("--hold-sec", type=int, default=15, help="Hold duration in seconds")

    args = parser.parse_args()
    exhaust_pool(args.host, args.port, args.db, args.user, args.password, args.connections, args.hold_sec)


if __name__ == "__main__":
    main()
