package io.github.javafromscratch.phase103;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 103: Low-Level Coordination: wait/notify Verification")
class Phase103DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase103Demo demo = new Phase103Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Low-Level Coordination: wait/notify"), "Output must contain lesson topic");
        assertTrue(result.contains("Always wait in a loop; never rely on solitary notify."), "Output must contain lesson motto");
    }
}
