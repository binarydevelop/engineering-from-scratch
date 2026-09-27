package io.github.javafromscratch.phase33;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 33: Immutable Domain Objects Verification")
class Phase33DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase33Demo demo = new Phase33Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Immutable Domain Objects"), "Output must contain lesson topic");
        assertTrue(result.contains("Immutable objects eliminate shared-mutable-state bugs across threads."), "Output must contain lesson motto");
    }
}
