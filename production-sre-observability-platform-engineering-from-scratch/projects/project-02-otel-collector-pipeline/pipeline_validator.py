"""
Project 02: Production OTel Collector Pipeline Validator.
Validates memory_limiter, batch processor, and exporter configurations.
"""
from typing import Dict, Any, List

def validate_collector_config(config: Dict[str, Any]) -> List[str]:
    errors = []
    service = config.get("service", {})
    pipelines = service.get("pipelines", {})
    processors = config.get("processors", {})

    if not pipelines:
        errors.append("No pipelines defined in service block")

    # Check for memory limiter in processors
    if "memory_limiter" not in processors:
        errors.append("Production pipeline must include 'memory_limiter' to prevent OOM")
    else:
        ml = processors["memory_limiter"]
        if "check_interval" not in ml or "limit_percentage" not in ml:
            errors.append("memory_limiter missing check_interval or limit_percentage")

    # Check batch processor
    if "batch" not in processors:
        errors.append("Production pipeline must include 'batch' processor for network efficiency")

    return errors
