package io.github.javafromscratch.phase12;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 12: The String Constant Pool Verification")
class Phase12DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase12Demo demo = new Phase12Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The String Constant Pool"), "Output must contain lesson topic");
        assertTrue(result.contains("The string pool is a JVM intern table deduplicating literal strings."), "Output must contain lesson motto");
    }
}
