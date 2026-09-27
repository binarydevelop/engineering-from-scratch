package io.github.javafromscratch.phase57;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 57: Exception Stack Trace Analysis Verification")
class Phase57DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase57Demo demo = new Phase57Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Exception Stack Trace Analysis"), "Output must contain lesson topic");
        assertTrue(result.contains("A stack trace is a photographic snapshot of the call stack at failure time."), "Output must contain lesson motto");
    }
}
