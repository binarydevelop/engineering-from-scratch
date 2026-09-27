"""
Fault-tolerant backend system wired with Chaos Injector and Resilience components.
"""

from typing import Dict, Any, Tuple
from chaos import ChaosInjector, DatabaseDropError, DatabaseTimeoutError
from resilience import CircuitBreaker, CircuitBreakerOpenError, CacheAsideManager

class ResilientBackendSystem:
    def __init__(self):
        self.chaos = ChaosInjector()
        self.db_records = {"prod_1": {"name": "High Availability Server", "price": 999}}
        self.cache = {}
        self.circuit_breaker = CircuitBreaker(failure_threshold=2, recovery_timeout_sec=0.2)
        self.cache_manager = CacheAsideManager(
            primary_db=self._read_db_primary,
            cache_store=self.cache
        )

    def _read_db_primary(self, key: str) -> Dict[str, Any]:
        self.chaos.maybe_fail_db()
        return self.db_records.get(key)

    def get_product(self, product_id: str) -> Tuple[int, Dict[str, Any]]:
        # Protect with circuit breaker
        try:
            def _fetch():
                return self.cache_manager.get_with_fallback(
                    product_id,
                    chaos_check=self.chaos.maybe_fail_cache
                )
            product = self.circuit_breaker.call(_fetch)
            if not product:
                return 404, {"error": "Not found"}
            return 200, product
        except CircuitBreakerOpenError:
            return 503, {"error": "Service temporarily degraded: Circuit Breaker OPEN", "code": "FAST_FAIL"}
        except DatabaseTimeoutError:
            return 504, {"error": "Gateway Timeout", "code": "DB_TIMEOUT"}
        except DatabaseDropError:
            return 503, {"error": "Database Unavailable", "code": "DB_DOWN"}
        except Exception as exc:
            return 500, {"error": "Internal Error", "detail": str(exc)}
