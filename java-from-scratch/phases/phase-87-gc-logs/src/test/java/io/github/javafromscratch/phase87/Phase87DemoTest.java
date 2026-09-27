package io.github.javafromscratch.phase87;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 87: GC Logging and Analysis Verification")
class Phase87DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase87Demo demo = new Phase87Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("GC Logging and Analysis"), "Output must contain lesson topic");
        assertTrue(result.contains("If you cannot see your GC pauses, you cannot guarantee your service SLAs."), "Output must contain lesson motto");
    }
}
