package io.github.javafromscratch.phase86;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 86: Modern GC: G1GC vs Generational ZGC Verification")
class Phase86DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase86Demo demo = new Phase86Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Modern GC: G1GC vs Generational ZGC"), "Output must contain lesson topic");
        assertTrue(result.contains("Modern GC trades minor CPU overhead for sub-millisecond pause guarantees."), "Output must contain lesson motto");
    }
}
