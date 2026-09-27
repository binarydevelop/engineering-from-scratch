package io.github.javafromscratch.phase199;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 199: Java in Modern Backend Engineering Verification")
class Phase199DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase199Demo demo = new Phase199Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Java in Modern Backend Engineering"), "Output must contain lesson topic");
        assertTrue(result.contains("Connect Java to Linux OS primitives, epoll, and cloud clusters."), "Output must contain lesson motto");
    }
}
