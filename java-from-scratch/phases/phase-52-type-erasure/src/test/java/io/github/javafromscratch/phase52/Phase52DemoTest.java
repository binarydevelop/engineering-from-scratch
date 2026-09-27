package io.github.javafromscratch.phase52;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 52: Type Erasure & Bytecode Reality Verification")
class Phase52DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase52Demo demo = new Phase52Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Type Erasure & Bytecode Reality"), "Output must contain lesson topic");
        assertTrue(result.contains("Generics exist purely for the compiler; the JVM bytecode knows almost nothing of them."), "Output must contain lesson motto");
    }
}
