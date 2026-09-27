package io.github.javafromscratch.phase45;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 45: Collection Performance & Selection Verification")
class Phase45DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase45Demo demo = new Phase45Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Collection Performance & Selection"), "Output must contain lesson topic");
        assertTrue(result.contains("Asymptotic Big-O describes scalability; hardware cache locality determines wall-clock time."), "Output must contain lesson motto");
    }
}
