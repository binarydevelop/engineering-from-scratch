package io.github.javafromscratch.phase188;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 188: Broken Lab 02: ConcurrentModificationException Verification")
class Phase188DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase188Demo demo = new Phase188Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Broken Lab 02: ConcurrentModificationException"), "Output must contain lesson topic");
        assertTrue(result.contains("Understand fail-fast collection iterators and modCount."), "Output must contain lesson motto");
    }
}
