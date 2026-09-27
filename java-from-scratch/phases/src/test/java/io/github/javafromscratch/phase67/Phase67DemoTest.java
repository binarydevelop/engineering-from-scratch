package io.github.javafromscratch.phase67;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 67: Lambdas: Anonymous Functions Verification")
class Phase67DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase67Demo demo = new Phase67Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Lambdas: Anonymous Functions"), "Output must contain lesson topic");
        assertTrue(result.contains("A lambda is code treated as data, desugared into invokedynamic calls."), "Output must contain lesson motto");
    }
}
