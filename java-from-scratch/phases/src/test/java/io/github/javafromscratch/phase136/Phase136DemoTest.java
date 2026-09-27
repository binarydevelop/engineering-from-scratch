package io.github.javafromscratch.phase136;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 136: Dependency Conflicts & Diamond Trees Verification")
class Phase136DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase136Demo demo = new Phase136Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Dependency Conflicts & Diamond Trees"), "Output must contain lesson topic");
        assertTrue(result.contains("Two versions of the same library on the classpath lead to runtime version roulette."), "Output must contain lesson motto");
    }
}
