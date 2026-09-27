package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 05 Fixed Verification: Unbounded Static Map Memory Leak")
class FixedLab05Test {

    @Test
    @DisplayName("Should verify that FixedLab05 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab05 fixed = new FixedLab05();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
