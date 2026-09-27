package io.github.javafromscratch.phase191;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 191: Broken Lab 05: Unbounded Static Memory Leak Verification")
class Phase191DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase191Demo demo = new Phase191Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 05: Unbounded Static Memory Leak"), "Output must contain lesson topic");
        assertTrue(result.contains("Find leaked references in static collections via heap dumps."), "Output must contain lesson motto");
    }
}
