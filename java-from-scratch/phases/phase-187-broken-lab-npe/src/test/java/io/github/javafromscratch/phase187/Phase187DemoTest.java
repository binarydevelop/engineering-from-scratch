package io.github.javafromscratch.phase187;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 187: Broken Lab 01: Hidden NullPointerException Verification")
class Phase187DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase187Demo demo = new Phase187Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 01: Hidden NullPointerException"), "Output must contain lesson topic");
        assertTrue(result.contains("Diagnose unboxing null traps and modern JVM NPE messages."), "Output must contain lesson motto");
    }
}
