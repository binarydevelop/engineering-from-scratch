package io.github.javafromscratch.phase109;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 109: Pipelines: CompletableFuture Verification")
class Phase109DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase109Demo demo = new Phase109Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Pipelines: CompletableFuture"), "Output must contain lesson topic");
        assertTrue(result.contains("Build non-blocking reactive pipelines via functional composition."), "Output must contain lesson motto");
    }
}
