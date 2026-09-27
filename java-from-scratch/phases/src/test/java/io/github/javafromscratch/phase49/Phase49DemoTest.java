package io.github.javafromscratch.phase49;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 49: Bounded Type Parameters Verification")
class Phase49DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase49Demo demo = new Phase49Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Bounded Type Parameters"), "Output must contain lesson topic");
        assertTrue(result.contains("Bounds restrict type parameters to types that support required capabilities."), "Output must contain lesson motto");
    }
}
