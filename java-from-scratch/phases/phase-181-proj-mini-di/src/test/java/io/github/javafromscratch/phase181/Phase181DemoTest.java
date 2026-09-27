package io.github.javafromscratch.phase181;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 181: Project 11: Mini Dependency Injection Container Verification")
class Phase181DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase181Demo demo = new Phase181Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 11: Mini Dependency Injection Container"), "Output must contain lesson topic");
        assertTrue(result.contains("Demystify frameworks by building constructor-based dependency injection."), "Output must contain lesson motto");
    }
}
