# Apache Druid Datasource Ingestion Spec
# Defines immutable time-chunked segments and ingestion-time rollup
import json
spec = {
    "type": "index_parallel",
    "spec": {
        "dataSchema": {
            "dataSource": "sensor_telemetry",
            "granularitySpec": {
                "type": "uniform",
                "segmentGranularity": "DAY",
                "queryGranularity": "MINUTE",
                "rollup": True
            }
        }
    }
}
print(json.dumps(spec, indent=2))
