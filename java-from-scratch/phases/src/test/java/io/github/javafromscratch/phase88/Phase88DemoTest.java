package io.github.javafromscratch.phase88;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 88: Heap Sizing & Container Memory Verification")
class Phase88DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase88Demo demo = new Phase88Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Heap Sizing & Container Memory"), "Output must contain lesson topic");
        assertTrue(result.contains("Setting heap too small causes GC thrashing; setting it too large causes paging."), "Output must contain lesson motto");
    }
}
