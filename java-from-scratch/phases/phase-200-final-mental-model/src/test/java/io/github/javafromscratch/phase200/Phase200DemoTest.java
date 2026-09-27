package io.github.javafromscratch.phase200;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 200: The Grand Unified Mental Model Verification")
class Phase200DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase200Demo demo = new Phase200Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The Grand Unified Mental Model"), "Output must contain lesson topic");
        assertTrue(result.contains("Trace a single HTTP request from socket through JVM to database and back."), "Output must contain lesson motto");
    }
}
