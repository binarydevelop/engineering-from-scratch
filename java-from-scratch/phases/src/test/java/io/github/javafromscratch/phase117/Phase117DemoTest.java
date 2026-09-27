package io.github.javafromscratch.phase117;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 117: Concurrency Architecture Comparison Verification")
class Phase117DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase117Demo demo = new Phase117Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Concurrency Architecture Comparison"), "Output must contain lesson topic");
        assertTrue(result.contains("Compare all concurrency models on an identical workload."), "Output must contain lesson motto");
    }
}
