package io.github.javafromscratch.phase56;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 56: Custom Domain Exceptions Verification")
class Phase56DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase56Demo demo = new Phase56Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Custom Domain Exceptions"), "Output must contain lesson topic");
        assertTrue(result.contains("Exceptions should carry structured domain context, not plain error strings."), "Output must contain lesson motto");
    }
}
