package io.github.javafromscratch.phase13;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 13: StringBuilder and Mutation Verification")
class Phase13DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase13Demo demo = new Phase13Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("StringBuilder and Mutation"), "Output must contain lesson topic");
        assertTrue(result.contains("Repeated string concatenation in loops is an O(N^2) allocation disaster."), "Output must contain lesson motto");
    }
}
