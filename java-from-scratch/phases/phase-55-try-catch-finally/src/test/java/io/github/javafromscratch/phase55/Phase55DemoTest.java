package io.github.javafromscratch.phase55;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 55: try, catch, and finally Mechanics Verification")
class Phase55DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase55Demo demo = new Phase55Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("try, catch, and finally Mechanics"), "Output must contain lesson topic");
        assertTrue(result.contains("finally blocks execute unconditionally, even in the presence of returns."), "Output must contain lesson motto");
    }
}
