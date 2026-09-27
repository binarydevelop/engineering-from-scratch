package io.github.javafromscratch.phase171;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 171: Project 1: Production CLI Application Verification")
class Phase171DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase171Demo demo = new Phase171Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 1: Production CLI Application"), "Output must contain lesson topic");
        assertTrue(result.contains("Build a production-grade CLI with parsing, configuration, and errors."), "Output must contain lesson motto");
    }
}
