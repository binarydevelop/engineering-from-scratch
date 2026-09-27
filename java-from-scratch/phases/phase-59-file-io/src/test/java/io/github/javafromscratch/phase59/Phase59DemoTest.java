package io.github.javafromscratch.phase59;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 59: File I/O Foundations Verification")
class Phase59DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase59Demo demo = new Phase59Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("File I/O Foundations"), "Output must contain lesson topic");
        assertTrue(result.contains("I/O is an operating system service mediated by kernel file descriptors."), "Output must contain lesson motto");
    }
}
