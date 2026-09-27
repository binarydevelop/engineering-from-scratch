package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 26 Fixed Verification: StringBuilder Repeated Resizing Overhead")
class FixedLab26Test {

    @Test
    @DisplayName("Should verify that FixedLab26 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab26 fixed = new FixedLab26();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
