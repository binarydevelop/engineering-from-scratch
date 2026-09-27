package io.github.javafromscratch.phase185;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 185: Project 15: High-Throughput Log Analyzer Verification")
class Phase185DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase185Demo demo = new Phase185Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 15: High-Throughput Log Analyzer"), "Output must contain lesson topic");
        assertTrue(result.contains("Stream multi-gigabyte log files and compute latency percentiles."), "Output must contain lesson motto");
    }
}
