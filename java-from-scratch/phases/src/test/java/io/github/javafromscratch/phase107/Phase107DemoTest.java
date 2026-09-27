package io.github.javafromscratch.phase107;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 107: Thread Pool Sizing Dynamics Verification")
class Phase107DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase107Demo demo = new Phase107Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Thread Pool Sizing Dynamics"), "Output must contain lesson topic");
        assertTrue(result.contains("Size CPU pools to cores; size I/O pools to blocking latency ratios."), "Output must contain lesson motto");
    }
}
