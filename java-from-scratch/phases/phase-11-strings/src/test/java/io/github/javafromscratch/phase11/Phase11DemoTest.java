package io.github.javafromscratch.phase11;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 11: Strings as Immutable Values Verification")
class Phase11DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase11Demo demo = new Phase11Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Strings as Immutable Values"), "Output must contain lesson topic");
        assertTrue(result.contains("Immutability guarantees safe sharing across threads and hash stability."), "Output must contain lesson motto");
    }
}
