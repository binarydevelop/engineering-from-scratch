package io.github.javafromscratch.phase164;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 164: Resource Lifecycle Management Verification")
class Phase164DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase164Demo demo = new Phase164Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Resource Lifecycle Management"), "Output must contain lesson topic");
        assertTrue(result.contains("Every socket, file descriptor, database handle, and thread pool must be explicitly closed."), "Output must contain lesson motto");
    }
}
