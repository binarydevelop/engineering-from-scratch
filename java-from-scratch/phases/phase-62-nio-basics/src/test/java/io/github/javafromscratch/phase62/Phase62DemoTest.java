package io.github.javafromscratch.phase62;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 62: Modern NIO Buffers and Channels Verification")
class Phase62DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase62Demo demo = new Phase62Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Modern NIO Buffers and Channels"), "Output must contain lesson topic");
        assertTrue(result.contains("NIO operates on memory buffers and direct channels without redundant copies."), "Output must contain lesson motto");
    }
}
