package io.github.javafromscratch.phase161;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 161: Essential JVM Tuning Flags Verification")
class Phase161DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase161Demo demo = new Phase161Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Essential JVM Tuning Flags"), "Output must contain lesson topic");
        assertTrue(result.contains("Use only flags you can justify with hard profiling data."), "Output must contain lesson motto");
    }
}
