package io.github.javafromscratch.phase48;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 48: Generic Methods Verification")
class Phase48DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase48Demo demo = new Phase48Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Generic Methods"), "Output must contain lesson topic");
        assertTrue(result.contains("A method can introduce its own type parameters independent of its enclosing class."), "Output must contain lesson motto");
    }
}
