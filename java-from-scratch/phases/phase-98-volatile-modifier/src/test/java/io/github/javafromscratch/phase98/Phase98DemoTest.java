package io.github.javafromscratch.phase98;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 98: The volatile Modifier Verification")
class Phase98DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase98Demo demo = new Phase98Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The volatile Modifier"), "Output must contain lesson topic");
        assertTrue(result.contains("volatile guarantees visibility and ordering, but NOT compound atomicity."), "Output must contain lesson motto");
    }
}
