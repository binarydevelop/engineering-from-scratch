package io.github.javafromscratch.phase126;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 126: ORM Motivation & Row Mapping Verification")
class Phase126DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase126Demo demo = new Phase126Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("ORM Motivation & Row Mapping"), "Output must contain lesson topic");
        assertTrue(result.contains("Understand the impedance mismatch between relational tables and object graphs."), "Output must contain lesson motto");
    }
}
