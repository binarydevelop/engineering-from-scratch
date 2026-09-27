package io.github.javafromscratch.phase27;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 27: Abstract Classes Verification")
class Phase27DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase27Demo demo = new Phase27Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Abstract Classes"), "Output must contain lesson topic");
        assertTrue(result.contains("An abstract class provides partial implementation and enforces template workflows."), "Output must contain lesson motto");
    }
}
