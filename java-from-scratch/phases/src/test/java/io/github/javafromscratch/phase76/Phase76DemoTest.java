package io.github.javafromscratch.phase76;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 76: Reflection from First Principles Verification")
class Phase76DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase76Demo demo = new Phase76Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Reflection from First Principles"), "Output must contain lesson topic");
        assertTrue(result.contains("Reflection lets code inspect and mutate its own structure at runtime."), "Output must contain lesson motto");
    }
}
