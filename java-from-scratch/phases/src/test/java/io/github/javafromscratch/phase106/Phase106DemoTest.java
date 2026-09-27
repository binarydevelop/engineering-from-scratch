package io.github.javafromscratch.phase106;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 106: Thread Pools: ExecutorService Verification")
class Phase106DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase106Demo demo = new Phase106Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Thread Pools: ExecutorService"), "Output must contain lesson topic");
        assertTrue(result.contains("Never spawn raw threads per request; pool and reuse them."), "Output must contain lesson motto");
    }
}
