package io.github.javafromscratch.phase122;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 122: JDBC from First Principles Verification")
class Phase122DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase122Demo demo = new Phase122Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("JDBC from First Principles"), "Output must contain lesson topic");
        assertTrue(result.contains("All Java database persistence reduces to raw JDBC drivers and sockets."), "Output must contain lesson motto");
    }
}
