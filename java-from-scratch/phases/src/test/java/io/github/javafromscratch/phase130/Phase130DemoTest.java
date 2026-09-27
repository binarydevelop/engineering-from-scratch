package io.github.javafromscratch.phase130;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 130: Build Tools from First Principles Verification")
class Phase130DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase130Demo demo = new Phase130Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Build Tools from First Principles"), "Output must contain lesson topic");
        assertTrue(result.contains("Build tools automate compilation, dependency resolution, testing, and packaging."), "Output must contain lesson motto");
    }
}
