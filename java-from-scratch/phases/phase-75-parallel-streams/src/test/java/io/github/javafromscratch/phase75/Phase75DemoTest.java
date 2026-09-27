package io.github.javafromscratch.phase75;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 75: Parallel Streams: Pitfalls & Reality Verification")
class Phase75DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase75Demo demo = new Phase75Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Parallel Streams: Pitfalls & Reality"), "Output must contain lesson topic");
        assertTrue(result.contains("Parallel streams do not automatically make code faster; often they make it slower."), "Output must contain lesson motto");
    }
}
