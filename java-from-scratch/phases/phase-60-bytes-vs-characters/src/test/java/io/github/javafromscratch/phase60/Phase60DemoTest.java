package io.github.javafromscratch.phase60;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 60: Bytes vs Characters & Encodings Verification")
class Phase60DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase60Demo demo = new Phase60Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Bytes vs Characters & Encodings"), "Output must contain lesson topic");
        assertTrue(result.contains("There is no such thing as plain text; there are only bytes and character encodings."), "Output must contain lesson motto");
    }
}
