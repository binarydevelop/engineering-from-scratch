package io.github.javafromscratch.phase156;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 156: Warmup Phenomena & Cold Starts Verification")
class Phase156DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase156Demo demo = new Phase156Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Warmup Phenomena & Cold Starts"), "Output must contain lesson topic");
        assertTrue(result.contains("A freshly started JVM runs in interpreted mode; give it time to optimize."), "Output must contain lesson motto");
    }
}
