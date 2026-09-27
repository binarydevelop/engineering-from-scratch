package io.github.javafromscratch.phase111;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 111: Concurrent Collections Verification")
class Phase111DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase111Demo demo = new Phase111Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Concurrent Collections"), "Output must contain lesson topic");
        assertTrue(result.contains("Concurrent collections eliminate coarse synchronized bottle-necks."), "Output must contain lesson motto");
    }
}
