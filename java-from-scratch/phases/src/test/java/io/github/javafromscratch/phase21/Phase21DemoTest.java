package io.github.javafromscratch.phase21;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 21: Static Members & Class State Verification")
class Phase21DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase21Demo demo = new Phase21Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Static Members & Class State"), "Output must contain lesson topic");
        assertTrue(result.contains("Static state is shared across all instances and lives for the classloader lifetime."), "Output must contain lesson motto");
    }
}
