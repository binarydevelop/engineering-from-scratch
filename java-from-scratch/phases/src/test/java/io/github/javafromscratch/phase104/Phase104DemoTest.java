package io.github.javafromscratch.phase104;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 104: Bounded Buffers: BlockingQueue Verification")
class Phase104DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase104Demo demo = new Phase104Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Bounded Buffers: BlockingQueue"), "Output must contain lesson topic");
        assertTrue(result.contains("BlockingQueue encapsulates thread coordination into safe put and take semantics."), "Output must contain lesson motto");
    }
}
