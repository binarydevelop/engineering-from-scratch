package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 35 Fixed Verification: StackOverflowError from Unbounded Recursion")
class FixedLab35Test {

    @Test
    @DisplayName("Should verify that FixedLab35 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab35 fixed = new FixedLab35();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
