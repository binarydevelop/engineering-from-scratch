package io.github.javafromscratch.phase179;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 179: Project 9: Distributed-Ready Rate Limiter Verification")
class Phase179DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase179Demo demo = new Phase179Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 9: Distributed-Ready Rate Limiter"), "Output must contain lesson topic");
        assertTrue(result.contains("Implement Token Bucket and Sliding Window rate limiting algorithms."), "Output must contain lesson motto");
    }
}
