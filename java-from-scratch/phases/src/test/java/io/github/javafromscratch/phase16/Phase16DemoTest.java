package io.github.javafromscratch.phase16;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 16: Constructors & Invariants Verification")
class Phase16DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase16Demo demo = new Phase16Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Constructors & Invariants"), "Output must contain lesson topic");
        assertTrue(result.contains("An object must never exist in an invalid state; invariants begin in the constructor."), "Output must contain lesson motto");
    }
}
