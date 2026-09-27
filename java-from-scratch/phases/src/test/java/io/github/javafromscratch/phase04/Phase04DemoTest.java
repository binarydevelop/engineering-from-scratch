package io.github.javafromscratch.phase04;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 04: Primitive vs Reference Types Verification")
class Phase04DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase04Demo demo = new Phase04Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Primitive vs Reference Types"), "Output must contain lesson topic");
        assertTrue(result.contains("Primitives hold values; references hold memory coordinates."), "Output must contain lesson motto");
    }
}
