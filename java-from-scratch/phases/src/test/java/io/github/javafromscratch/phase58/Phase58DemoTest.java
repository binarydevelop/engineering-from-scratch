package io.github.javafromscratch.phase58;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 58: Try-With-Resources & AutoCloseable Verification")
class Phase58DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase58Demo demo = new Phase58Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Try-With-Resources & AutoCloseable"), "Output must contain lesson topic");
        assertTrue(result.contains("Manual resource cleanup will eventually leak; automate it with AutoCloseable."), "Output must contain lesson motto");
    }
}
