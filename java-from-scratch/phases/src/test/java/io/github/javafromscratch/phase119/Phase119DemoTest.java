package io.github.javafromscratch.phase119;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 119: Modern HTTP Client (java.net.http) Verification")
class Phase119DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase119Demo demo = new Phase119Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Modern HTTP Client (java.net.http)"), "Output must contain lesson topic");
        assertTrue(result.contains("Issue resilient HTTP requests with modern asynchronous HTTP clients."), "Output must contain lesson motto");
    }
}
