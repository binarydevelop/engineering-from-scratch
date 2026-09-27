package io.github.javafromscratch.phase91;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 91: Memory Leaks in GC Languages Verification")
class Phase91DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase91Demo demo = new Phase91Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Memory Leaks in GC Languages"), "Output must contain lesson topic");
        assertTrue(result.contains("An object is leaked in Java if it remains reachable but is never used again."), "Output must contain lesson motto");
    }
}
