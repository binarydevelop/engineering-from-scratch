package io.github.javafromscratch.phase54;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 54: Checked vs Unchecked Exceptions Verification")
class Phase54DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase54Demo demo = new Phase54Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Checked vs Unchecked Exceptions"), "Output must contain lesson topic");
        assertTrue(result.contains("Recoverable environmental faults are checked; programmer defects are unchecked."), "Output must contain lesson motto");
    }
}
