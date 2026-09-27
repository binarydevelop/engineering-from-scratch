package io.github.javafromscratch.phase14;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 14: Classes: State and Behavior Verification")
class Phase14DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase14Demo demo = new Phase14Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Classes: State and Behavior"), "Output must contain lesson topic");
        assertTrue(result.contains("A class defines a type, encapsulation boundaries, and invariant enforcement."), "Output must contain lesson motto");
    }
}
