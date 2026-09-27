package io.github.javafromscratch.phase07;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 07: Control Flow & Pattern Matching Verification")
class Phase07DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase07Demo demo = new Phase07Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Control Flow & Pattern Matching"), "Output must contain lesson topic");
        assertTrue(result.contains("Control flow translates to conditional jumps in the operand stack."), "Output must contain lesson motto");
    }
}
