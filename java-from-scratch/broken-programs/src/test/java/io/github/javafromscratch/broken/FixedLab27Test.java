package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 27 Fixed Verification: Virtual Thread Pinned to Carrier in synchronized")
class FixedLab27Test {

    @Test
    @DisplayName("Should verify that FixedLab27 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab27 fixed = new FixedLab27();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
