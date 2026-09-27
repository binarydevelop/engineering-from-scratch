package io.github.javafromscratch.phase01;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 01: Source -> Bytecode -> JVM Verification")
class Phase01DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase01Demo demo = new Phase01Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Source -> Bytecode -> JVM"), "Output must contain lesson topic");
        assertTrue(result.contains("Java source is for humans; bytecode is for the virtual machine."), "Output must contain lesson motto");
    }
}
