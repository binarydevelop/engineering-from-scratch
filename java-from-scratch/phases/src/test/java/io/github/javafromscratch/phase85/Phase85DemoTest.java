package io.github.javafromscratch.phase85;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 85: Generational Garbage Collection Verification")
class Phase85DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase85Demo demo = new Phase85Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Generational Garbage Collection"), "Output must contain lesson topic");
        assertTrue(result.contains("The Weak Generational Hypothesis: Most allocated objects die young."), "Output must contain lesson motto");
    }
}
