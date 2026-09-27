package io.github.javafromscratch.phase51;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 51: The PECS Principle Verification")
class Phase51DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase51Demo demo = new Phase51Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The PECS Principle"), "Output must contain lesson topic");
        assertTrue(result.contains("Use ? extends T when reading data out; use ? super T when putting data in."), "Output must contain lesson motto");
    }
}
