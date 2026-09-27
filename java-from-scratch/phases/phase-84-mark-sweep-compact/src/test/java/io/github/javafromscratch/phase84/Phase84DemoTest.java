package io.github.javafromscratch.phase84;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 84: Mark, Sweep, and Compact Algorithms Verification")
class Phase84DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase84Demo demo = new Phase84Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Mark, Sweep, and Compact Algorithms"), "Output must contain lesson topic");
        assertTrue(result.contains("Marking identifies liveness; sweeping reclaims; compacting cures fragmentation."), "Output must contain lesson motto");
    }
}
