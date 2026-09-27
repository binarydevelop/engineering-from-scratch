# ClickHouse Real-Time Ingestion & Materialization Verification
import clickhouse_connect
try:
    client = clickhouse_connect.get_client(host='127.0.0.1', port=8123, username='default', password='clickhouse')
    res = client.command('SELECT version()')
    print('ClickHouse Connected:', res)
except Exception as e:
    print('ClickHouse container offline. Run make docker-up.')
