package io.github.javafromscratch.phase170;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 170: The Native Boundary & JNI/FFM Verification")
class Phase170DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase170Demo demo = new Phase170Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The Native Boundary & JNI/FFM"), "Output must contain lesson topic");
        assertTrue(result.contains("The JVM interacts with the operating system kernel and hardware via native code."), "Output must contain lesson motto");
    }
}
