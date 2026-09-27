package io.github.javafromscratch.phase145;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 145: Configuration Management Verification")
class Phase145DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase145Demo demo = new Phase145Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Configuration Management"), "Output must contain lesson topic");
        assertTrue(result.contains("Strictly separate code from configuration across environments."), "Output must contain lesson motto");
    }
}
