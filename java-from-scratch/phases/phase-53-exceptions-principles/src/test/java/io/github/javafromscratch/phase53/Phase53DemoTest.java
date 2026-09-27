package io.github.javafromscratch.phase53;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 53: Exceptions from First Principles Verification")
class Phase53DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase53Demo demo = new Phase53Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Exceptions from First Principles"), "Output must contain lesson topic");
        assertTrue(result.contains("Exceptions provide out-of-band communication of invariant violations."), "Output must contain lesson motto");
    }
}
