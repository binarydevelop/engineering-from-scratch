package io.github.javafromscratch.phase93;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 93: Thread Lifecycle & State Transitions Verification")
class Phase93DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase93Demo demo = new Phase93Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Thread Lifecycle & State Transitions"), "Output must contain lesson topic");
        assertTrue(result.contains("Understand every transition between NEW, RUNNABLE, BLOCKED, and WAITING."), "Output must contain lesson motto");
    }
}
