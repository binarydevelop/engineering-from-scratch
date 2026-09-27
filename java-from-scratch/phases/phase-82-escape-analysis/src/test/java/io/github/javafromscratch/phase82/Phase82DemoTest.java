package io.github.javafromscratch.phase82;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 82: Escape Analysis & Scalar Replacement Verification")
class Phase82DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase82Demo demo = new Phase82Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Escape Analysis & Scalar Replacement"), "Output must contain lesson topic");
        assertTrue(result.contains("HotSpot does not allocate objects on the stack; it replaces them with scalars."), "Output must contain lesson motto");
    }
}
