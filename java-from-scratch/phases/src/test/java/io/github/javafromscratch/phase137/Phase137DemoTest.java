package io.github.javafromscratch.phase137;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 137: Testing from First Principles Verification")
class Phase137DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase137Demo demo = new Phase137Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Testing from First Principles"), "Output must contain lesson topic");
        assertTrue(result.contains("A test is an executable assertion that verifies an invariant under controlled conditions."), "Output must contain lesson motto");
    }
}
