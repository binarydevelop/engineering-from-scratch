package io.github.javafromscratch.phase189;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 189: Broken Lab 03: Classpath Catastrophe Verification")
class Phase189DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase189Demo demo = new Phase189Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 03: Classpath Catastrophe"), "Output must contain lesson topic");
        assertTrue(result.contains("Untangle ClassNotFoundException vs NoClassDefFoundError."), "Output must contain lesson motto");
    }
}
