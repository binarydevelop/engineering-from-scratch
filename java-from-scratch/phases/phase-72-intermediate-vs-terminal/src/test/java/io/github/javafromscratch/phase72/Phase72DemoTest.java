package io.github.javafromscratch.phase72;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 72: Intermediate vs Terminal Operations Verification")
class Phase72DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase72Demo demo = new Phase72Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Intermediate vs Terminal Operations"), "Output must contain lesson topic");
        assertTrue(result.contains("Intermediate stream operations do nothing until a terminal operation demands results."), "Output must contain lesson motto");
    }
}
