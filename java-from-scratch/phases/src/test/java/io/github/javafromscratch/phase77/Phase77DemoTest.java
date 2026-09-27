package io.github.javafromscratch.phase77;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 77: Custom Annotations & Processing Verification")
class Phase77DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase77Demo demo = new Phase77Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Custom Annotations & Processing"), "Output must contain lesson topic");
        assertTrue(result.contains("Annotations attach metadata to code elements to power framework discovery."), "Output must contain lesson motto");
    }
}
