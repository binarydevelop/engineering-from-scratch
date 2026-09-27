package io.github.javafromscratch.phase02;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 02: The main Method Dissected Verification")
class Phase02DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase02Demo demo = new Phase02Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The main Method Dissected"), "Output must contain lesson topic");
        assertTrue(result.contains("Every keyword in the entry point is an architectural contract."), "Output must contain lesson motto");
    }
}
