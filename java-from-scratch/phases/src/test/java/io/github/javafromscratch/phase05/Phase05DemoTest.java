package io.github.javafromscratch.phase05;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 05: Numeric Behavior and Overflow Verification")
class Phase05DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase05Demo demo = new Phase05Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Numeric Behavior and Overflow"), "Output must contain lesson topic");
        assertTrue(result.contains("Computers do not do ideal arithmetic; they do bounded binary arithmetic."), "Output must contain lesson motto");
    }
}
