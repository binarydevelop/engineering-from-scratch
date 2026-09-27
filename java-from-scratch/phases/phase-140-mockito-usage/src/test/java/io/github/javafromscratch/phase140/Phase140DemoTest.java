package io.github.javafromscratch.phase140;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 140: Mockito: Usage and Misuse Verification")
class Phase140DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase140Demo demo = new Phase140Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Mockito: Usage and Misuse"), "Output must contain lesson topic");
        assertTrue(result.contains("Mock at architectural boundaries; never mock domain models or simple values."), "Output must contain lesson motto");
    }
}
