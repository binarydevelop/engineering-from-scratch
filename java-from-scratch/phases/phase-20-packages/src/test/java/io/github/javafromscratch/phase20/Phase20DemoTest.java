package io.github.javafromscratch.phase20;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 20: Packages and Namespaces Verification")
class Phase20DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase20Demo demo = new Phase20Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Packages and Namespaces"), "Output must contain lesson topic");
        assertTrue(result.contains("Packages partition the global type space and enforce directory structures."), "Output must contain lesson motto");
    }
}
