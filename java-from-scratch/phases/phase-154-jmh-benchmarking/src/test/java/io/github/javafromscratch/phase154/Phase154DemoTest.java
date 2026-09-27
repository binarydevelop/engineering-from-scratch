package io.github.javafromscratch.phase154;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 154: Rigorous Microbenchmarking with JMH Verification")
class Phase154DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase154Demo demo = new Phase154Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Rigorous Microbenchmarking with JMH"), "Output must contain lesson topic");
        assertTrue(result.contains("Never trust a naive timer loop; use JMH to defeat JIT optimizations."), "Output must contain lesson motto");
    }
}
