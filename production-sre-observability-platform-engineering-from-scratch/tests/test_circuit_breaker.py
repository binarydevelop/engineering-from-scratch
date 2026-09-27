import time
import unittest
from services.common.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException, CircuitState


class TestCircuitBreaker(unittest.TestCase):
    def test_circuit_trips_on_consecutive_failures(self):
        cb = CircuitBreaker("test-gateway", failure_threshold=3, recovery_timeout_sec=0.1)
        self.assertEqual(cb.state, CircuitState.CLOSED)

        def failing_func():
            raise ConnectionResetError("Connection dropped")

        # First 2 failures: circuit remains closed
        for _ in range(2):
            with self.assertRaises(ConnectionResetError):
                cb.call(failing_func)
            self.assertEqual(cb.state, CircuitState.CLOSED)

        # 3rd failure: circuit trips to OPEN
        with self.assertRaises(ConnectionResetError):
            cb.call(failing_func)
        self.assertEqual(cb.state, CircuitState.OPEN)

        # 4th call: fails fast with CircuitBreakerOpenException immediately
        with self.assertRaises(CircuitBreakerOpenException):
            cb.call(failing_func)

        # Wait for recovery timeout
        time.sleep(0.12)
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, CircuitState.HALF_OPEN)

        # Successful probe call resets circuit to CLOSED
        def successful_func():
            return "ok"

        res = cb.call(successful_func)
        self.assertEqual(res, "ok")
        self.assertEqual(cb.state, CircuitState.CLOSED)


if __name__ == "__main__":
    unittest.main()
