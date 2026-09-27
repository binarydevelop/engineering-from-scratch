package io.github.javafromscratch.phase25;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 25: Polymorphism & Dispatch Verification")
class Phase25DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase25Demo demo = new Phase25Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Polymorphism & Dispatch"), "Output must contain lesson topic");
        assertTrue(result.contains("Variables have static compile types; objects have dynamic runtime types."), "Output must contain lesson motto");
    }
}
