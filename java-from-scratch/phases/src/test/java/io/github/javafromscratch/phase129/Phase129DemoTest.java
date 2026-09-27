package io.github.javafromscratch.phase129;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 129: Lazy Loading & Detached Entities Verification")
class Phase129DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase129Demo demo = new Phase129Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Lazy Loading & Detached Entities"), "Output must contain lesson topic");
        assertTrue(result.contains("Accessing lazy properties outside an active transaction throws LazyInitializationException."), "Output must contain lesson motto");
    }
}
