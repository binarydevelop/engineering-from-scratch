package io.github.javafromscratch.phase64;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 64: Modern Date and Time (java.time) Verification")
class Phase64DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase64Demo demo = new Phase64Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Modern Date and Time (java.time)"), "Output must contain lesson topic");
        assertTrue(result.contains("Time is a physical continuum; calendars are geopolitical conventions."), "Output must contain lesson motto");
    }
}
