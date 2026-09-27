package io.github.javafromscratch.phase195;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 195: Broken Lab 09: Slow Startup & Initializer Lockup Verification")
class Phase195DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase195Demo demo = new Phase195Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 09: Slow Startup & Initializer Lockup"), "Output must contain lesson topic");
        assertTrue(result.contains("Profile blocking work inside static initializers."), "Output must contain lesson motto");
    }
}
