package io.github.javafromscratch.phase134;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 134: Anatomy of a JAR File Verification")
class Phase134DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase134Demo demo = new Phase134Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Anatomy of a JAR File"), "Output must contain lesson topic");
        assertTrue(result.contains("A JAR is a ZIP archive with a META-INF/MANIFEST.MF contract."), "Output must contain lesson motto");
    }
}
