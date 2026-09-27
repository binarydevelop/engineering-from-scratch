package io.github.javafromscratch.phase50;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 50: Generics Subtyping and Wildcards Verification")
class Phase50DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase50Demo demo = new Phase50Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Generics Subtyping and Wildcards"), "Output must contain lesson topic");
        assertTrue(result.contains("List<Integer> is NOT a subtype of List<Number>."), "Output must contain lesson motto");
    }
}
