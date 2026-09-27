package io.github.javafromscratch.phase105;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 105: High-Throughput Producer-Consumer Verification")
class Phase105DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase105Demo demo = new Phase105Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("High-Throughput Producer-Consumer"), "Output must contain lesson topic");
        assertTrue(result.contains("Decouple processing stages with bounded queues to smooth traffic bursts."), "Output must contain lesson motto");
    }
}
