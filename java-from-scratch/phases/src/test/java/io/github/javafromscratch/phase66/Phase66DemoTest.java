package io.github.javafromscratch.phase66;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 66: Optional Done Right Verification")
class Phase66DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase66Demo demo = new Phase66Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Optional Done Right"), "Output must contain lesson topic");
        assertTrue(result.contains("Optional is a return-type signal for absent values, not a field replacement."), "Output must contain lesson motto");
    }
}
