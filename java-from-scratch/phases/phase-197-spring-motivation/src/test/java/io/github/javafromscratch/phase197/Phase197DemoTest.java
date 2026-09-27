package io.github.javafromscratch.phase197;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 197: Deconstructing the Spring Framework Verification")
class Phase197DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase197Demo demo = new Phase197Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Deconstructing the Spring Framework"), "Output must contain lesson topic");
        assertTrue(result.contains("Map framework abstractions to core Java primitives."), "Output must contain lesson motto");
    }
}
