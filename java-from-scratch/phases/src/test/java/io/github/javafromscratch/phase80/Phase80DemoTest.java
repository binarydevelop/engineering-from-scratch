package io.github.javafromscratch.phase80;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 80: Stack Frames & Operand Stack Verification")
class Phase80DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase80Demo demo = new Phase80Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Stack Frames & Operand Stack"), "Output must contain lesson topic");
        assertTrue(result.contains("JVM execution is a stack of frames containing local variables and operand stacks."), "Output must contain lesson motto");
    }
}
