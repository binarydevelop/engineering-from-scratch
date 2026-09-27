package io.github.javafromscratch.phase120;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 120: Building a Minimal HTTP Server Verification")
class Phase120DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase120Demo demo = new Phase120Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Building a Minimal HTTP Server"), "Output must contain lesson topic");
        assertTrue(result.contains("An HTTP server is a socket server parsing headers and returning text lines."), "Output must contain lesson motto");
    }
}
