package io.github.javafromscratch.phase115;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 115: Platform vs Virtual Threads Benchmark Verification")
class Phase115DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase115Demo demo = new Phase115Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Platform vs Virtual Threads Benchmark"), "Output must contain lesson topic");
        assertTrue(result.contains("Virtual threads excel at high-concurrency blocking I/O, not CPU-bound math."), "Output must contain lesson motto");
    }
}
