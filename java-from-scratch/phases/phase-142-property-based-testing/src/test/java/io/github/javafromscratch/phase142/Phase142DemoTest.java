package io.github.javafromscratch.phase142;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 142: Property-Based Invariant Testing Verification")
class Phase142DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase142Demo demo = new Phase142Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Property-Based Invariant Testing"), "Output must contain lesson topic");
        assertTrue(result.contains("Generate thousands of random inputs to discover corner cases you never imagined."), "Output must contain lesson motto");
    }
}
