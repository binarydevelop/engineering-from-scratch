package io.github.javafromscratch.phase114;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 114: Modern Virtual Threads (Project Loom) Verification")
class Phase114DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase114Demo demo = new Phase114Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Modern Virtual Threads (Project Loom)"), "Output must contain lesson topic");
        assertTrue(result.contains("Virtual threads make thread-per-request cheap again."), "Output must contain lesson motto");
    }
}
