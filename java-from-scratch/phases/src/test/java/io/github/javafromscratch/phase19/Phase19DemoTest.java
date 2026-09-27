package io.github.javafromscratch.phase19;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 19: Access Modifiers Architecture Verification")
class Phase19DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase19Demo demo = new Phase19Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Access Modifiers Architecture"), "Output must contain lesson topic");
        assertTrue(result.contains("Access modifiers define API visibility and module packaging boundaries."), "Output must contain lesson motto");
    }
}
