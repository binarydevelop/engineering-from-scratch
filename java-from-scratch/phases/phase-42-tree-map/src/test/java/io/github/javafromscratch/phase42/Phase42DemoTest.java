package io.github.javafromscratch.phase42;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 42: TreeMap & TreeSet Verification")
class Phase42DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase42Demo demo = new Phase42Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("TreeMap & TreeSet"), "Output must contain lesson topic");
        assertTrue(result.contains("Self-balancing binary search trees provide guaranteed O(log N) sorted operations."), "Output must contain lesson motto");
    }
}
