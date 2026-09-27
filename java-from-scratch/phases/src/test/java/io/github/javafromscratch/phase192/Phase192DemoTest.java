package io.github.javafromscratch.phase192;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 192: Broken Lab 06: GC Thrashing & Allocation Storm Verification")
class Phase192DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase192Demo demo = new Phase192Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 06: GC Thrashing & Allocation Storm"), "Output must contain lesson topic");
        assertTrue(result.contains("Profile excessive temporary allocations causing GC latency spikes."), "Output must contain lesson motto");
    }
}
