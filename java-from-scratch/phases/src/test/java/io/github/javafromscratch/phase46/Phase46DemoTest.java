package io.github.javafromscratch.phase46;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 46: The Motivation for Generics Verification")
class Phase46DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase46Demo demo = new Phase46Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The Motivation for Generics"), "Output must contain lesson topic");
        assertTrue(result.contains("Cast errors should be caught at compile time, not in production."), "Output must contain lesson motto");
    }
}
