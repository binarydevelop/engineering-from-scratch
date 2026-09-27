package io.github.javafromscratch.phase44;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 44: PriorityQueue from Scratch Verification")
class Phase44DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase44Demo demo = new Phase44Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("PriorityQueue from Scratch"), "Output must contain lesson topic");
        assertTrue(result.contains("A binary heap maintains the extreme element at the root in O(1)."), "Output must contain lesson motto");
    }
}
