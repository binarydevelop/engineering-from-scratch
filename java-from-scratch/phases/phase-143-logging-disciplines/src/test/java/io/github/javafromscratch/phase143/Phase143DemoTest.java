package io.github.javafromscratch.phase143;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 143: Production Logging Disciplines Verification")
class Phase143DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase143Demo demo = new Phase143Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Production Logging Disciplines"), "Output must contain lesson topic");
        assertTrue(result.contains("Never use System.out.println in production; emit structured, leveled telemetry."), "Output must contain lesson motto");
    }
}
