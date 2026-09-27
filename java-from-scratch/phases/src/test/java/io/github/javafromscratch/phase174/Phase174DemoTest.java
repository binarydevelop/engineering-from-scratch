package io.github.javafromscratch.phase174;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 174: Project 4: Concurrent Task Runner Verification")
class Phase174DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase174Demo demo = new Phase174Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 4: Concurrent Task Runner"), "Output must contain lesson topic");
        assertTrue(result.contains("Build a resilient concurrent task runner with retries and cancellation."), "Output must contain lesson motto");
    }
}
