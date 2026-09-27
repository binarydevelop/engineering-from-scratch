package io.github.javafromscratch.phase193;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 193: Broken Lab 07: Thread Pool Exhaustion Verification")
class Phase193DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase193Demo demo = new Phase193Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 07: Thread Pool Exhaustion"), "Output must contain lesson topic");
        assertTrue(result.contains("Diagnose thread pool starvation caused by blocking tasks."), "Output must contain lesson motto");
    }
}
