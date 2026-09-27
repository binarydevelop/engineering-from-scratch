package io.github.javafromscratch.phase09;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 09: Pass-by-Value Mechanics Verification")
class Phase09DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase09Demo demo = new Phase09Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Pass-by-Value Mechanics"), "Output must contain lesson topic");
        assertTrue(result.contains("Java is strictly pass-by-value: references are passed by value."), "Output must contain lesson motto");
    }
}
