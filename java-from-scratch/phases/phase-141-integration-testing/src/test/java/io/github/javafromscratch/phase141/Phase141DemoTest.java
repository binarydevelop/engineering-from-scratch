package io.github.javafromscratch.phase141;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 141: Integration Testing & Real DBs Verification")
class Phase141DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase141Demo demo = new Phase141Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Integration Testing & Real DBs"), "Output must contain lesson topic");
        assertTrue(result.contains("Unit tests verify logic; integration tests verify communication with real dependencies."), "Output must contain lesson motto");
    }
}
