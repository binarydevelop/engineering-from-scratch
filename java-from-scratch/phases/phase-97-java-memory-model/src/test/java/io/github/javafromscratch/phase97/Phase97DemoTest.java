package io.github.javafromscratch.phase97;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 97: The Java Memory Model (JMM) Verification")
class Phase97DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase97Demo demo = new Phase97Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The Java Memory Model (JMM)"), "Output must contain lesson topic");
        assertTrue(result.contains("The JMM is a contract between the JVM, compiler, hardware, and programmer."), "Output must contain lesson motto");
    }
}
