package io.github.javafromscratch.phase94;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 94: Race Conditions & Data Races Verification")
class Phase94DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase94Demo demo = new Phase94Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Race Conditions & Data Races"), "Output must contain lesson topic");
        assertTrue(result.contains("When concurrent threads mutate shared state without synchronization, chaos ensues."), "Output must contain lesson motto");
    }
}
