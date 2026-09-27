package io.github.javafromscratch.phase73;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 73: Collectors & Reductions Verification")
class Phase73DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase73Demo demo = new Phase73Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Collectors & Reductions"), "Output must contain lesson topic");
        assertTrue(result.contains("Collectors fold stream elements into complex downstream data structures."), "Output must contain lesson motto");
    }
}
