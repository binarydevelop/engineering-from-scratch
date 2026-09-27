package io.github.javafromscratch.phase121;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 121: Serialization Boundaries & JSON Verification")
class Phase121DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase121Demo demo = new Phase121Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Serialization Boundaries & JSON"), "Output must contain lesson topic");
        assertTrue(result.contains("Validate and deserialize external untrusted payloads at the network boundary."), "Output must contain lesson motto");
    }
}
