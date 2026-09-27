package io.github.javafromscratch.phase163;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 163: Defensive Security in Java Verification")
class Phase163DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase163Demo demo = new Phase163Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Defensive Security in Java"), "Output must contain lesson topic");
        assertTrue(result.contains("Never trust input; validate boundaries; avoid unsafe reflection and deserialization."), "Output must contain lesson motto");
    }
}
