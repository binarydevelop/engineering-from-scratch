package io.github.javafromscratch.phase99;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 99: Atomic Variables & Hardware CAS Verification")
class Phase99DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase99Demo demo = new Phase99Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Atomic Variables & Hardware CAS"), "Output must contain lesson topic");
        assertTrue(result.contains("Lock-free algorithms use hardware compare-and-swap to achieve non-blocking concurrency."), "Output must contain lesson motto");
    }
}
