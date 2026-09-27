package io.github.javafromscratch.phase133;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 133: Gradle Architecture Overview Verification")
class Phase133DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase133Demo demo = new Phase133Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Gradle Architecture Overview"), "Output must contain lesson topic");
        assertTrue(result.contains("Gradle provides incremental builds and domain-specific configuration."), "Output must contain lesson motto");
    }
}
