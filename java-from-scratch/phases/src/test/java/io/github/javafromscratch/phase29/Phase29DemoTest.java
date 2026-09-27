package io.github.javafromscratch.phase29;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 29: Composition over Inheritance Verification")
class Phase29DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase29Demo demo = new Phase29Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Composition over Inheritance"), "Output must contain lesson topic");
        assertTrue(result.contains("Favor 'has-a' over 'is-a' to build flexible, testable architectures."), "Output must contain lesson motto");
    }
}
