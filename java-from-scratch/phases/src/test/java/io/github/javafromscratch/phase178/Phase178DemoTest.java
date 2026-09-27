package io.github.javafromscratch.phase178;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 178: Project 8: Generic Thread-Safe LRU Cache Verification")
class Phase178DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase178Demo demo = new Phase178Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 8: Generic Thread-Safe LRU Cache"), "Output must contain lesson topic");
        assertTrue(result.contains("Implement an O(1) generic LRU cache with fine-grained concurrency locking."), "Output must contain lesson motto");
    }
}
