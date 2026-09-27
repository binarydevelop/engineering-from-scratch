package io.github.javafromscratch.phase06;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 06: Operators and Expressions Verification")
class Phase06DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase06Demo demo = new Phase06Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Operators and Expressions"), "Output must contain lesson topic");
        assertTrue(result.contains("Short-circuit evaluation is both a performance guard and a null defense."), "Output must contain lesson motto");
    }
}
