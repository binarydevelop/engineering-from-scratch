package io.github.javafromscratch.phase176;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 176: Project 6: Lightweight HTTP Server Verification")
class Phase176DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase176Demo demo = new Phase176Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 6: Lightweight HTTP Server"), "Output must contain lesson topic");
        assertTrue(result.contains("Build an HTTP/1.1 server from raw TCP sockets with virtual threads."), "Output must contain lesson motto");
    }
}
