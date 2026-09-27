package io.github.javafromscratch.phase23;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 23: Records: Data Carriers Verification")
class Phase23DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase23Demo demo = new Phase23Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Records: Data Carriers"), "Output must contain lesson topic");
        assertTrue(result.contains("When data is just data, use a record for unambiguous immutability."), "Output must contain lesson motto");
    }
}
