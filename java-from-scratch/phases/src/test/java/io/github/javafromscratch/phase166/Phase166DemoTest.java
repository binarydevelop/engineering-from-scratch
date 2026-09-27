package io.github.javafromscratch.phase166;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 166: JVM Shutdown Hooks Verification")
class Phase166DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase166Demo demo = new Phase166Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("JVM Shutdown Hooks"), "Output must contain lesson topic");
        assertTrue(result.contains("Shutdown hooks run during JVM termination; keep them fast and non-deadlocking."), "Output must contain lesson motto");
    }
}
