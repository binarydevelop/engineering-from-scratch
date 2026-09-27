package io.github.javafromscratch.phase196;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 196: Broken Lab 10: 35+ Production Debugging Suite Verification")
class Phase196DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase196Demo demo = new Phase196Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 10: 35+ Production Debugging Suite"), "Output must contain lesson topic");
        assertTrue(result.contains("Master diagnostic root cause analysis across 35 realistic failures."), "Output must contain lesson motto");
    }
}
