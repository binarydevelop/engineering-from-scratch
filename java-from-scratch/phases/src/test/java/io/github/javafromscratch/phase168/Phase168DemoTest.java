package io.github.javafromscratch.phase168;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 168: Pluggable Architecture: ServiceLoader Verification")
class Phase168DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase168Demo demo = new Phase168Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Pluggable Architecture: ServiceLoader"), "Output must contain lesson topic");
        assertTrue(result.contains("ServiceLoader discovers interface implementations dynamically at runtime."), "Output must contain lesson motto");
    }
}
