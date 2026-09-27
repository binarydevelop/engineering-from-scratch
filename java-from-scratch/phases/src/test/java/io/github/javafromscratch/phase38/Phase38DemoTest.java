package io.github.javafromscratch.phase38;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 38: LinkedList from Scratch Verification")
class Phase38DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase38Demo demo = new Phase38Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("LinkedList from Scratch"), "Output must contain lesson topic");
        assertTrue(result.contains("Pointers provide O(1) insertions at known positions but destroy cache locality."), "Output must contain lesson motto");
    }
}
