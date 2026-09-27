package io.github.javafromscratch.phase172;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 172: Project 2: Banking Domain Engine Verification")
class Phase172DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase172Demo demo = new Phase172Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 2: Banking Domain Engine"), "Output must contain lesson topic");
        assertTrue(result.contains("Implement strict invariant validation, Money, and concurrent transfers."), "Output must contain lesson motto");
    }
}
