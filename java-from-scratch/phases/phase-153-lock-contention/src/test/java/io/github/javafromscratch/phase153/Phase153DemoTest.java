package io.github.javafromscratch.phase153;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 153: Lock Contention & Amdahl's Law Verification")
class Phase153DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase153Demo demo = new Phase153Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Lock Contention & Amdahl's Law"), "Output must contain lesson topic");
        assertTrue(result.contains("Amdahl's Law: The speedup of a program is limited by its serial fraction."), "Output must contain lesson motto");
    }
}
