package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 22 Fixed Verification: Blocking I/O Inside Common ForkJoinPool")
class FixedLab22Test {

    @Test
    @DisplayName("Should verify that FixedLab22 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab22 fixed = new FixedLab22();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
