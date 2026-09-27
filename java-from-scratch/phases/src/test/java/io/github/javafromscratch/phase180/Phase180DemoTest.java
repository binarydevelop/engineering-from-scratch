package io.github.javafromscratch.phase180;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 180: Project 10: In-Memory Message Broker Verification")
class Phase180DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase180Demo demo = new Phase180Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 10: In-Memory Message Broker"), "Output must contain lesson topic");
        assertTrue(result.contains("Build an educational pub/sub message broker with bounded queues."), "Output must contain lesson motto");
    }
}
