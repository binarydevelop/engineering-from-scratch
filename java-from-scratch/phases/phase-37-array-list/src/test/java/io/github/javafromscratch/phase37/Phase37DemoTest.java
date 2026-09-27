package io.github.javafromscratch.phase37;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 37: ArrayList from Scratch Verification")
class Phase37DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase37Demo demo = new Phase37Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("ArrayList from Scratch"), "Output must contain lesson topic");
        assertTrue(result.contains("Contiguous memory guarantees O(1) random access and cache line locality."), "Output must contain lesson motto");
    }
}
