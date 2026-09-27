package io.github.javafromscratch.phase194;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 194: Broken Lab 08: Leaked JDBC Connection Pool Verification")
class Phase194DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase194Demo demo = new Phase194Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 08: Leaked JDBC Connection Pool"), "Output must contain lesson topic");
        assertTrue(result.contains("Diagnose unclosed database connections exhausting the pool."), "Output must contain lesson motto");
    }
}
