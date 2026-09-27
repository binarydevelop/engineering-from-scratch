package io.github.javafromscratch.phase71;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 71: Stream vs Collection Architecture Verification")
class Phase71DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase71Demo demo = new Phase71Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Stream vs Collection Architecture"), "Output must contain lesson topic");
        assertTrue(result.contains("A collection is space-bound; a stream is time-bound and single-use."), "Output must contain lesson motto");
    }
}
