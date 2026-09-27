package io.github.javafromscratch.phase24;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 24: Inheritance & Subtyping Verification")
class Phase24DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase24Demo demo = new Phase24Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Inheritance & Subtyping"), "Output must contain lesson topic");
        assertTrue(result.contains("Inheritance is for 'is-a' substitution, not a code-reuse shortcut."), "Output must contain lesson motto");
    }
}
