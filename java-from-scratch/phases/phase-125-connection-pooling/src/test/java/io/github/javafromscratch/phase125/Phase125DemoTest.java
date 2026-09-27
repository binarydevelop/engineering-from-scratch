package io.github.javafromscratch.phase125;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 125: Database Connection Pooling Verification")
class Phase125DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase125Demo demo = new Phase125Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Database Connection Pooling"), "Output must contain lesson topic");
        assertTrue(result.contains("Opening a TCP connection to a database per request will crush database performance."), "Output must contain lesson motto");
    }
}
