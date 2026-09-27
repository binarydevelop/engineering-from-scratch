package io.github.javafromscratch.phase22;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 22: Enums as Finite Sets Verification")
class Phase22DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase22Demo demo = new Phase22Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Enums as Finite Sets"), "Output must contain lesson topic");
        assertTrue(result.contains("An enum is a full Java class with guaranteed singleton instances."), "Output must contain lesson motto");
    }
}
