package io.github.javafromscratch.phase152;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 152: Allocation Profiling & GC Pressure Verification")
class Phase152DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase152Demo demo = new Phase152Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Allocation Profiling & GC Pressure"), "Output must contain lesson topic");
        assertTrue(result.contains("The fastest garbage collection is the one that never has to run."), "Output must contain lesson motto");
    }
}
