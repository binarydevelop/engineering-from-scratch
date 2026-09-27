package io.github.javafromscratch.phase43;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 43: Queues and Deques Verification")
class Phase43DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase43Demo demo = new Phase43Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Queues and Deques"), "Output must contain lesson topic");
        assertTrue(result.contains("Queues enforce temporal ordering: First-In, First-Out."), "Output must contain lesson motto");
    }
}
