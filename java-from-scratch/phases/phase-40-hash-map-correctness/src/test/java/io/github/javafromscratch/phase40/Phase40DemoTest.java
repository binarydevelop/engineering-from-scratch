package io.github.javafromscratch.phase40;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 40: HashMap Correctness & Mutable Keys Verification")
class Phase40DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase40Demo demo = new Phase40Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("HashMap Correctness & Mutable Keys"), "Output must contain lesson topic");
        assertTrue(result.contains("Never use a mutable object as a hash map key."), "Output must contain lesson motto");
    }
}
