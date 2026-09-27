package io.github.javafromscratch.phase158;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 158: Escape Analysis in Practice Verification")
class Phase158DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase158Demo demo = new Phase158Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Escape Analysis in Practice"), "Output must contain lesson topic");
        assertTrue(result.contains("If an object does not escape, C2 eliminates heap allocation entirely."), "Output must contain lesson motto");
    }
}
