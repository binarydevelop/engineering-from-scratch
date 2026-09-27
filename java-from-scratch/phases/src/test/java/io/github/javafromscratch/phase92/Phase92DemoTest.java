package io.github.javafromscratch.phase92;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 92: Threads from First Principles Verification")
class Phase92DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase92Demo demo = new Phase92Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Threads from First Principles"), "Output must contain lesson topic");
        assertTrue(result.contains("A thread is an independent execution context sharing memory with other threads."), "Output must contain lesson motto");
    }
}
