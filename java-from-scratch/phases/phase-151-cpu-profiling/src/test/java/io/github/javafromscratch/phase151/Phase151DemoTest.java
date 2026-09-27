package io.github.javafromscratch.phase151;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 151: CPU Profiling: Hot Path Optimization Verification")
class Phase151DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase151Demo demo = new Phase151Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("CPU Profiling: Hot Path Optimization"), "Output must contain lesson topic");
        assertTrue(result.contains("Optimize the 5% of code where the CPU spends 90% of its cycles."), "Output must contain lesson motto");
    }
}
