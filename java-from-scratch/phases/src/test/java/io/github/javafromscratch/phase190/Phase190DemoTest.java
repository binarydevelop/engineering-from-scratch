package io.github.javafromscratch.phase190;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 190: Broken Lab 04: Multi-Threaded Deadlock Verification")
class Phase190DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase190Demo demo = new Phase190Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 04: Multi-Threaded Deadlock"), "Output must contain lesson topic");
        assertTrue(result.contains("Diagnose circular lock dependencies using jcmd thread dumps."), "Output must contain lesson motto");
    }
}
