package io.github.javafromscratch.phase167;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 167: Java Platform Module System Verification")
class Phase167DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase167Demo demo = new Phase167Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Java Platform Module System"), "Output must contain lesson topic");
        assertTrue(result.contains("Modules enforce strong encapsulation across package boundaries at the JVM level."), "Output must contain lesson motto");
    }
}
