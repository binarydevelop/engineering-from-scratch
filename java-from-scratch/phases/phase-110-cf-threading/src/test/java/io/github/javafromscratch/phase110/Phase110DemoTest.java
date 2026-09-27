package io.github.javafromscratch.phase110;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 110: CompletableFuture Threading Rules Verification")
class Phase110DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase110Demo demo = new Phase110Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("CompletableFuture Threading Rules"), "Output must contain lesson topic");
        assertTrue(result.contains("Know which executor runs each stage of your async pipeline."), "Output must contain lesson motto");
    }
}
