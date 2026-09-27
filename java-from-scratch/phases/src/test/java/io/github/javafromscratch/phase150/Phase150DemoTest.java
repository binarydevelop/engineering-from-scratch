package io.github.javafromscratch.phase150;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 150: JDK Mission Control (JMC) Verification")
class Phase150DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase150Demo demo = new Phase150Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("JDK Mission Control (JMC)"), "Output must contain lesson topic");
        assertTrue(result.contains("Visualize JFR recordings to isolate latency spikes and memory hotspots."), "Output must contain lesson motto");
    }
}
