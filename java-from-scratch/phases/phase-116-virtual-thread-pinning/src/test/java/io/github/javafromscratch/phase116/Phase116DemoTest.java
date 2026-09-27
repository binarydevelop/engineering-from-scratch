package io.github.javafromscratch.phase116;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 116: Virtual Thread Pinning Caveats Verification")
class Phase116DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase116Demo demo = new Phase116Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Virtual Thread Pinning Caveats"), "Output must contain lesson topic");
        assertTrue(result.contains("synchronized blocks pin virtual threads to carrier threads; use ReentrantLock."), "Output must contain lesson motto");
    }
}
