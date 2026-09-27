package io.github.javafromscratch.phase36;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 36: Collections Framework Overview Verification")
class Phase36DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase36Demo demo = new Phase36Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Collections Framework Overview"), "Output must contain lesson topic");
        assertTrue(result.contains("Choose collections by required access semantics, not by habit."), "Output must contain lesson motto");
    }
}
