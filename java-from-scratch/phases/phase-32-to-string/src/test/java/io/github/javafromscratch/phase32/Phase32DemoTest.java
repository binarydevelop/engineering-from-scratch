package io.github.javafromscratch.phase32;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 32: toString Diagnostic Reps Verification")
class Phase32DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase32Demo demo = new Phase32Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("toString Diagnostic Reps"), "Output must contain lesson topic");
        assertTrue(result.contains("toString is for engineers debugging systems at 3 AM; keep it precise."), "Output must contain lesson motto");
    }
}
