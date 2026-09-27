package io.github.javafromscratch.phase28;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 28: Interfaces as Contracts Verification")
class Phase28DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase28Demo demo = new Phase28Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Interfaces as Contracts"), "Output must contain lesson topic");
        assertTrue(result.contains("Interfaces decouple what a component does from how it is implemented."), "Output must contain lesson motto");
    }
}
