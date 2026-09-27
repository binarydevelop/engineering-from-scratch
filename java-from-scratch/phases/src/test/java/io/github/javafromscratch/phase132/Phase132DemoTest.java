package io.github.javafromscratch.phase132;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 132: Maven Dependency Scopes Verification")
class Phase132DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase132Demo demo = new Phase132Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Maven Dependency Scopes"), "Output must contain lesson topic");
        assertTrue(result.contains("Scopes restrict library visibility across compilation, testing, and runtime."), "Output must contain lesson motto");
    }
}
