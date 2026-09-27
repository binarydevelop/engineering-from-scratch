package io.github.javafromscratch.phase17;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 17: The this Reference Verification")
class Phase17DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase17Demo demo = new Phase17Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The this Reference"), "Output must contain lesson topic");
        assertTrue(result.contains("this is the hidden zeroth argument passed to every instance method."), "Output must contain lesson motto");
    }
}
