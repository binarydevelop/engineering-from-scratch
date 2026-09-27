package io.github.javafromscratch.phase149;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 149: Java Flight Recorder (JFR) Verification")
class Phase149DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase149Demo demo = new Phase149Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Java Flight Recorder (JFR)"), "Output must contain lesson topic");
        assertTrue(result.contains("Record continuous, low-overhead event telemetry directly from the HotSpot kernel."), "Output must contain lesson motto");
    }
}
