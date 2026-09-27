package io.github.javafromscratch.phase198;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 198: Inspecting Framework Bytecode & Proxies Verification")
class Phase198DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase198Demo demo = new Phase198Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Inspecting Framework Bytecode & Proxies"), "Output must contain lesson topic");
        assertTrue(result.contains("Disassemble dynamic JDK proxies and CGLIB bytecode generation."), "Output must contain lesson motto");
    }
}
