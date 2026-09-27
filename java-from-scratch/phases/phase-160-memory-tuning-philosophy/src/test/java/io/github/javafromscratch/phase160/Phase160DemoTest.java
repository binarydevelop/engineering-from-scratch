package io.github.javafromscratch.phase160;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 160: Memory Tuning Philosophy Verification")
class Phase160DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase160Demo demo = new Phase160Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Memory Tuning Philosophy"), "Output must contain lesson topic");
        assertTrue(result.contains("Fix application memory leaks and allocation churn before touching JVM flags."), "Output must contain lesson motto");
    }
}
