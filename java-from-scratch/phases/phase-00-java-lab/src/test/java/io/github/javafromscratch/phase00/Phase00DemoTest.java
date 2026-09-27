package io.github.javafromscratch.phase00;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 00: Java Lab & Environment Verification")
class Phase00DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase00Demo demo = new Phase00Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Java Lab & Environment"), "Output must contain lesson topic");
        assertTrue(result.contains("Before you write code, verify the compiler and runtime."), "Output must contain lesson motto");
    }
}
