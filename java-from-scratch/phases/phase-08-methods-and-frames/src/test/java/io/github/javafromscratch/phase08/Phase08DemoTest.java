package io.github.javafromscratch.phase08;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 08: Methods and Stack Execution Verification")
class Phase08DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase08Demo demo = new Phase08Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Methods and Stack Execution"), "Output must contain lesson topic");
        assertTrue(result.contains("A method call is a new activation frame pushed onto the thread stack."), "Output must contain lesson motto");
    }
}
