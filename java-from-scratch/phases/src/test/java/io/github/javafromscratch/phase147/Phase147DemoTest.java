package io.github.javafromscratch.phase147;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 147: Stack Trace Forensics Verification")
class Phase147DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase147Demo demo = new Phase147Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Stack Trace Forensics"), "Output must contain lesson topic");
        assertTrue(result.contains("Read stack traces backwards from the ultimate root cause."), "Output must contain lesson motto");
    }
}
