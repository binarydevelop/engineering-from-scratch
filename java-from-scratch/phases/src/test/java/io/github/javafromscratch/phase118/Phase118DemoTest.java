package io.github.javafromscratch.phase118;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 118: TCP Sockets from Scratch Verification")
class Phase118DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase118Demo demo = new Phase118Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("TCP Sockets from Scratch"), "Output must contain lesson topic");
        assertTrue(result.contains("Network programming is reading and writing byte streams over OS sockets."), "Output must contain lesson motto");
    }
}
