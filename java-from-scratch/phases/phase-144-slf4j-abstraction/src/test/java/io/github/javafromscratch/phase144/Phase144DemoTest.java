package io.github.javafromscratch.phase144;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 144: SLF4J Facade Architecture Verification")
class Phase144DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase144Demo demo = new Phase144Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("SLF4J Facade Architecture"), "Output must contain lesson topic");
        assertTrue(result.contains("Code against the SLF4J logging facade; bind the logging backend at runtime."), "Output must contain lesson motto");
    }
}
