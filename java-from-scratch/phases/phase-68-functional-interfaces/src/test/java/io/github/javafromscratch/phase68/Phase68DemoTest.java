package io.github.javafromscratch.phase68;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 68: Core Functional Interfaces Verification")
class Phase68DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase68Demo demo = new Phase68Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Core Functional Interfaces"), "Output must contain lesson topic");
        assertTrue(result.contains("Standardize behavioral signatures with standard functional interfaces."), "Output must contain lesson motto");
    }
}
