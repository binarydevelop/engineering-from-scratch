package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 07 Fixed Verification: Thread Pool Exhaustion / Starvation")
class FixedLab07Test {

    @Test
    @DisplayName("Should verify that FixedLab07 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab07 fixed = new FixedLab07();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
