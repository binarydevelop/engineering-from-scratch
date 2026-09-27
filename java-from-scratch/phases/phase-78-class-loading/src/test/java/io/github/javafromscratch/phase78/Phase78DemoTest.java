package io.github.javafromscratch.phase78;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 78: Class Loading & Custom Loaders Verification")
class Phase78DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase78Demo demo = new Phase78Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Class Loading & Custom Loaders"), "Output must contain lesson topic");
        assertTrue(result.contains("A class in the JVM is identified by its fully qualified name AND its ClassLoader."), "Output must contain lesson motto");
    }
}
