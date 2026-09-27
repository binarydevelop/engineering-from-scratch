package io.github.javafromscratch.phase26;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 26: Method Overriding vs Overloading Verification")
class Phase26DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase26Demo demo = new Phase26Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Method Overriding vs Overloading"), "Output must contain lesson topic");
        assertTrue(result.contains("Overloading is resolved statically at compile time; overriding dynamically at runtime."), "Output must contain lesson motto");
    }
}
