package io.github.javafromscratch.phase03;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 03: Variables and Primitive Types Verification")
class Phase03DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase03Demo demo = new Phase03Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Variables and Primitive Types"), "Output must contain lesson topic");
        assertTrue(result.contains("Memory is a fixed grid of bits; types determine interpretation."), "Output must contain lesson motto");
    }
}
