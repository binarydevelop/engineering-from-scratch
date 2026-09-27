package io.github.javafromscratch.phase18;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 18: Encapsulation & Invariants Verification")
class Phase18DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase18Demo demo = new Phase18Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Encapsulation & Invariants"), "Output must contain lesson topic");
        assertTrue(result.contains("Exposing internal representation invites external corruption."), "Output must contain lesson motto");
    }
}
