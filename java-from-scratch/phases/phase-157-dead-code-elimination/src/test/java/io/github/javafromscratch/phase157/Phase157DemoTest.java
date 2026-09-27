package io.github.javafromscratch.phase157;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 157: Dead Code & Constant Folding Verification")
class Phase157DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase157Demo demo = new Phase157Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Dead Code & Constant Folding"), "Output must contain lesson topic");
        assertTrue(result.contains("The C2 compiler ruthlessly deletes code whose results are never observed."), "Output must contain lesson motto");
    }
}
