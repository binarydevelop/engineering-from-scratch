package io.github.javafromscratch.phase74;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 74: Streams vs Loops Performance Verification")
class Phase74DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase74Demo demo = new Phase74Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Streams vs Loops Performance"), "Output must contain lesson topic");
        assertTrue(result.contains("Write for humans first; optimize with loops only when profiling proves necessary."), "Output must contain lesson motto");
    }
}
