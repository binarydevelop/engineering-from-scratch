package io.github.javafromscratch.phase34;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 34: Primitive Wrapper Types Verification")
class Phase34DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase34Demo demo = new Phase34Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Primitive Wrapper Types"), "Output must contain lesson topic");
        assertTrue(result.contains("Wrappers bridge primitives to object-oriented generics at the cost of heap allocation."), "Output must contain lesson motto");
    }
}
