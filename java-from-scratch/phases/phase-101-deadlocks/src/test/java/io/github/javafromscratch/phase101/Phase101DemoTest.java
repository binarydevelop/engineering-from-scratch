package io.github.javafromscratch.phase101;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 101: Deadlocks: Creation & Prevention Verification")
class Phase101DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase101Demo demo = new Phase101Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Deadlocks: Creation & Prevention"), "Output must contain lesson topic");
        assertTrue(result.contains("Deadlock occurs when circular lock acquisition dependencies form."), "Output must contain lesson motto");
    }
}
