package io.github.javafromscratch.phase35;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 35: Autoboxing & Pitfalls Verification")
class Phase35DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase35Demo demo = new Phase35Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Autoboxing & Pitfalls"), "Output must contain lesson topic");
        assertTrue(result.contains("Autoboxing conceals object allocations and injects hidden null hazards."), "Output must contain lesson motto");
    }
}
