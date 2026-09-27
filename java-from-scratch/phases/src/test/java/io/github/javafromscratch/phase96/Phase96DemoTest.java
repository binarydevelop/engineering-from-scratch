package io.github.javafromscratch.phase96;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 96: Memory Visibility & CPU Caching Verification")
class Phase96DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase96Demo demo = new Phase96Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Memory Visibility & CPU Caching"), "Output must contain lesson topic");
        assertTrue(result.contains("Without synchronization, a thread may never observe writes made by another."), "Output must contain lesson motto");
    }
}
