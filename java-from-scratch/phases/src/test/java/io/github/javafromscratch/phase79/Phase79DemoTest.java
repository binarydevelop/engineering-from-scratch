package io.github.javafromscratch.phase79;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 79: JVM Runtime Memory Areas Verification")
class Phase79DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase79Demo demo = new Phase79Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("JVM Runtime Memory Areas"), "Output must contain lesson topic");
        assertTrue(result.contains("Understand every byte allocated in the JVM process address space."), "Output must contain lesson motto");
    }
}
