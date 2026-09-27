package io.github.javafromscratch.phase138;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 138: Modern JUnit 5 Deep Dive Verification")
class Phase138DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase138Demo demo = new Phase138Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Modern JUnit 5 Deep Dive"), "Output must contain lesson topic");
        assertTrue(result.contains("JUnit 5 structures assertions, lifecycles, and parameterized test executions."), "Output must contain lesson motto");
    }
}
