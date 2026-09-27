package io.github.javafromscratch.phase102;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 102: Thread Dumps & Deadlock Analysis Verification")
class Phase102DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase102Demo demo = new Phase102Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Thread Dumps & Deadlock Analysis"), "Output must contain lesson topic");
        assertTrue(result.contains("A thread dump cuts through deadlocks and stuck threads instantly."), "Output must contain lesson motto");
    }
}
