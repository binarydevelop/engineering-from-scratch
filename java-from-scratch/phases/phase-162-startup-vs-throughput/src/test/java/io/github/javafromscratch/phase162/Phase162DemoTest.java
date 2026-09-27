package io.github.javafromscratch.phase162;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 162: Startup Latency vs Throughput Verification")
class Phase162DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase162Demo demo = new Phase162Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Startup Latency vs Throughput"), "Output must contain lesson topic");
        assertTrue(result.contains("CLI tools require fast startup; server backends require high peak throughput."), "Output must contain lesson motto");
    }
}
