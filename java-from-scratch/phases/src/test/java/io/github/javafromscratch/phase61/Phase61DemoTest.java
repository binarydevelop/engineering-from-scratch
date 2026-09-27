package io.github.javafromscratch.phase61;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 61: Buffered I/O & Syscall Overhead Verification")
class Phase61DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase61Demo demo = new Phase61Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Buffered I/O & Syscall Overhead"), "Output must contain lesson topic");
        assertTrue(result.contains("Issuing a kernel syscall for every byte is a 1000x performance penalty."), "Output must contain lesson motto");
    }
}
