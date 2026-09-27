package io.github.javafromscratch.phase65;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 65: Precision Money with BigDecimal Verification")
class Phase65DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase65Demo demo = new Phase65Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Precision Money with BigDecimal"), "Output must contain lesson topic");
        assertTrue(result.contains("Never represent monetary currency with floating-point types."), "Output must contain lesson motto");
    }
}
