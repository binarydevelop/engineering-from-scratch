package io.github.javafromscratch.phase47;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 47: Generic Classes & Containers Verification")
class Phase47DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase47Demo demo = new Phase47Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Generic Classes & Containers"), "Output must contain lesson topic");
        assertTrue(result.contains("Type parameters parameterize code over types with compile-time verification."), "Output must contain lesson motto");
    }
}
