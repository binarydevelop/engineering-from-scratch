package io.github.javafromscratch.phase155;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 155: JIT Compilation: Bytecode to Native Verification")
class Phase155DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase155Demo demo = new Phase155Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("JIT Compilation: Bytecode to Native"), "Output must contain lesson topic");
        assertTrue(result.contains("HotSpot compiles only hot code, dynamically optimizing for actual runtime data."), "Output must contain lesson motto");
    }
}
