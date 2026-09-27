package io.github.javafromscratch.phase159;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 159: The Performance Methodology Verification")
class Phase159DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase159Demo demo = new Phase159Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The Performance Methodology"), "Output must contain lesson topic");
        assertTrue(result.contains("Hypothesis-driven tuning: Measure -> Profile -> Hypothesize -> Modify -> Verify."), "Output must contain lesson motto");
    }
}
