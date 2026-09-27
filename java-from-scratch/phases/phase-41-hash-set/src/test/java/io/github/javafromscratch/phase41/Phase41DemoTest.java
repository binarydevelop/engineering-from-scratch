package io.github.javafromscratch.phase41;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 41: HashSet from Scratch Verification")
class Phase41DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase41Demo demo = new Phase41Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("HashSet from Scratch"), "Output must contain lesson topic");
        assertTrue(result.contains("A set is simply a hash map where the values are ignored."), "Output must contain lesson motto");
    }
}
