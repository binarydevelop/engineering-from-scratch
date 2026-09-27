package io.github.javafromscratch.phase173;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 173: Project 3: Library Management System Verification")
class Phase173DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase173Demo demo = new Phase173Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 3: Library Management System"), "Output must contain lesson topic");
        assertTrue(result.contains("Model domain rules with collections, interfaces, and custom exceptions."), "Output must contain lesson motto");
    }
}
