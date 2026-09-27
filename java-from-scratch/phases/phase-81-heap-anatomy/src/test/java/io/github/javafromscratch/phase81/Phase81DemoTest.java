package io.github.javafromscratch.phase81;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 81: The Heap & Compressed OOPs Verification")
class Phase81DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase81Demo demo = new Phase81Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The Heap & Compressed OOPs"), "Output must contain lesson topic");
        assertTrue(result.contains("Heap memory is managed globally; compressed OOPs save 40% memory below 32GB."), "Output must contain lesson motto");
    }
}
