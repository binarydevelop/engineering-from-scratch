package io.github.javafromscratch.phase113;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 113: CountDownLatch & CyclicBarrier Verification")
class Phase113DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase113Demo demo = new Phase113Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("CountDownLatch & CyclicBarrier"), "Output must contain lesson topic");
        assertTrue(result.contains("Synchronize thread progress at designated computational checkpoints."), "Output must contain lesson motto");
    }
}
