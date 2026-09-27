package io.github.javafromscratch.phase39;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 39: HashMap from First Principles Verification")
class Phase39DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase39Demo demo = new Phase39Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("HashMap from First Principles"), "Output must contain lesson topic");
        assertTrue(result.contains("Hash functions project infinite key spaces into finite bucket arrays."), "Output must contain lesson motto");
    }
}
