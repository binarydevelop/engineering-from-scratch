package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 16 Fixed Verification: ThreadLocal Leak in Recycled Thread Pool")
class FixedLab16Test {

    @Test
    @DisplayName("Should verify that FixedLab16 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab16 fixed = new FixedLab16();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
