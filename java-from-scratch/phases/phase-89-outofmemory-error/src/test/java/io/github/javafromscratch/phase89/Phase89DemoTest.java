package io.github.javafromscratch.phase89;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 89: OutOfMemoryError Taxonomy Verification")
class Phase89DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase89Demo demo = new Phase89Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("OutOfMemoryError Taxonomy"), "Output must contain lesson topic");
        assertTrue(result.contains("Not all OOM errors are heap leaks; diagnose the exact memory area."), "Output must contain lesson motto");
    }
}
