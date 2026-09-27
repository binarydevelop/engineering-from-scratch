package io.github.javafromscratch.phase165;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 165: Graceful Shutdown Architecture Verification")
class Phase165DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase165Demo demo = new Phase165Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Graceful Shutdown Architecture"), "Output must contain lesson topic");
        assertTrue(result.contains("A production service must finish in-flight requests before exiting on SIGTERM."), "Output must contain lesson motto");
    }
}
