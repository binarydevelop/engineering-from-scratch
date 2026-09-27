package io.github.javafromscratch.phase169;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 169: Annotation Processing (APT) Verification")
class Phase169DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase169Demo demo = new Phase169Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Annotation Processing (APT)"), "Output must contain lesson topic");
        assertTrue(result.contains("Generate code at compile-time to avoid runtime reflection overhead."), "Output must contain lesson motto");
    }
}
