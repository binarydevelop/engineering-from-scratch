package io.github.javafromscratch.phase69;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 69: Method References Verification")
class Phase69DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase69Demo demo = new Phase69Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Method References"), "Output must contain lesson topic");
        assertTrue(result.contains("Method references make existing methods first-class functional values."), "Output must contain lesson motto");
    }
}
