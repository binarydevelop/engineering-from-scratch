package io.github.javafromscratch.phase15;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 15: Objects on the Heap Verification")
class Phase15DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase15Demo demo = new Phase15Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Objects on the Heap"), "Output must contain lesson topic");
        assertTrue(result.contains("A class is metadata in Metaspace; an object is live data on the Heap."), "Output must contain lesson motto");
    }
}
