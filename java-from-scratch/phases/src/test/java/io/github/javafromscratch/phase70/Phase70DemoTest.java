package io.github.javafromscratch.phase70;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 70: Streams: Declarative Pipelines Verification")
class Phase70DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase70Demo demo = new Phase70Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Streams: Declarative Pipelines"), "Output must contain lesson topic");
        assertTrue(result.contains("Collections store data in memory; streams compute data through pipelines."), "Output must contain lesson motto");
    }
}
