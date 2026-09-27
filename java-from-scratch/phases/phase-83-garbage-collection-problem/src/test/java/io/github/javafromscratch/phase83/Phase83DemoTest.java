package io.github.javafromscratch.phase83;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 83: The Garbage Collection Problem Verification")
class Phase83DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase83Demo demo = new Phase83Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The Garbage Collection Problem"), "Output must contain lesson topic");
        assertTrue(result.contains("Manual memory management leads to leaks and dangling pointers; GC guarantees safety."), "Output must contain lesson motto");
    }
}
