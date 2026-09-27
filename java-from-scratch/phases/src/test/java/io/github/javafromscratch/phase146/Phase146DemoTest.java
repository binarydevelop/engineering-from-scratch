package io.github.javafromscratch.phase146;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 146: Interactive Debugging & JDWP Verification")
class Phase146DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase146Demo demo = new Phase146Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Interactive Debugging & JDWP"), "Output must contain lesson topic");
        assertTrue(result.contains("The debugger connects to the JVM socket to inspect variables and control execution."), "Output must contain lesson motto");
    }
}
