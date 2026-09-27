package io.github.javafromscratch.phase95;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 95: Intrinsic Locks & synchronized Verification")
class Phase95DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase95Demo demo = new Phase95Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Intrinsic Locks & synchronized"), "Output must contain lesson topic");
        assertTrue(result.contains("synchronized establishes mutual exclusion and memory visibility across threads."), "Output must contain lesson motto");
    }
}
