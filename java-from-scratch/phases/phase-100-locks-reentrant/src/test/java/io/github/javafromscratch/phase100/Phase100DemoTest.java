package io.github.javafromscratch.phase100;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 100: Explicit Locks: ReentrantLock Verification")
class Phase100DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase100Demo demo = new Phase100Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Explicit Locks: ReentrantLock"), "Output must contain lesson topic");
        assertTrue(result.contains("ReentrantLock provides timed, interruptible, and fair lock acquisition."), "Output must contain lesson motto");
    }
}
