package io.github.javafromscratch.phase30;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 30: Object Equality: == vs equals Verification")
class Phase30DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase30Demo demo = new Phase30Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Object Equality: == vs equals"), "Output must contain lesson topic");
        assertTrue(result.contains("== tests pointer identity; equals tests semantic value equivalence."), "Output must contain lesson motto");
    }
}
