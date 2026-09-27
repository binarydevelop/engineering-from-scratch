package io.github.javafromscratch.phase148;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 148: jcmd: HotSpot Diagnostics Verification")
class Phase148DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase148Demo demo = new Phase148Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("jcmd: HotSpot Diagnostics"), "Output must contain lesson topic");
        assertTrue(result.contains("Inspect and control any live JVM process with zero external instrumentation."), "Output must contain lesson motto");
    }
}
