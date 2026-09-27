package io.github.javafromscratch.phase108;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 108: Asynchronous Results: Future Verification")
class Phase108DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase108Demo demo = new Phase108Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Asynchronous Results: Future"), "Output must contain lesson topic");
        assertTrue(result.contains("A Future is a handle to a computation that completes in the future."), "Output must contain lesson motto");
    }
}
