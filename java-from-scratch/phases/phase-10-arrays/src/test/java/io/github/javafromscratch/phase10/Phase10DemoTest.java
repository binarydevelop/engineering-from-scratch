package io.github.javafromscratch.phase10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 10: Arrays from First Principles Verification")
class Phase10DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase10Demo demo = new Phase10Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Arrays from First Principles"), "Output must contain lesson topic");
        assertTrue(result.contains("An array is a contiguous, fixed-size heap allocation with bounds checks."), "Output must contain lesson motto");
    }
}
