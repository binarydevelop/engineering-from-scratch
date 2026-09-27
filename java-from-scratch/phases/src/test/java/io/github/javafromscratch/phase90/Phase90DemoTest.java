package io.github.javafromscratch.phase90;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 90: Heap Dumps & Object Forensics Verification")
class Phase90DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase90Demo demo = new Phase90Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Heap Dumps & Object Forensics"), "Output must contain lesson topic");
        assertTrue(result.contains("A heap dump captures the exact object graph at the moment of failure."), "Output must contain lesson motto");
    }
}
