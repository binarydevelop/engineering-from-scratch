package io.github.javafromscratch.phase63;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 63: Serialization Boundaries & JSON Verification")
class Phase63DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase63Demo demo = new Phase63Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Serialization Boundaries & JSON"), "Output must contain lesson topic");
        assertTrue(result.contains("Java native serialization is a security minefield; prefer explicit text/binary protocols."), "Output must contain lesson motto");
    }
}
