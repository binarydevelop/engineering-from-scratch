package io.github.javafromscratch.phase139;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 139: Test Doubles: Fakes, Stubs, Mocks Verification")
class Phase139DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase139Demo demo = new Phase139Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Test Doubles: Fakes, Stubs, Mocks"), "Output must contain lesson topic");
        assertTrue(result.contains("Fakes have working implementations; stubs return canned data; mocks verify interactions."), "Output must contain lesson motto");
    }
}
