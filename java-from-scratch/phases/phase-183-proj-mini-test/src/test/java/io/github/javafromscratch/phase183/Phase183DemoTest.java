package io.github.javafromscratch.phase183;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 183: Project 13: Mini Test Framework Verification")
class Phase183DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase183Demo demo = new Phase183Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 13: Mini Test Framework"), "Output must contain lesson topic");
        assertTrue(result.contains("Build a JUnit-like test discovery and execution framework from scratch."), "Output must contain lesson motto");
    }
}
