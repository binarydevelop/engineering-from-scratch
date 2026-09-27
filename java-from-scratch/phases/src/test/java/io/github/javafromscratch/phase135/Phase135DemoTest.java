package io.github.javafromscratch.phase135;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 135: The Classpath: Mechanics & Disasters Verification")
class Phase135DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase135Demo demo = new Phase135Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The Classpath: Mechanics & Disasters"), "Output must contain lesson topic");
        assertTrue(result.contains("The classpath is an ordered list of directories and JARs scanned for .class files."), "Output must contain lesson motto");
    }
}
