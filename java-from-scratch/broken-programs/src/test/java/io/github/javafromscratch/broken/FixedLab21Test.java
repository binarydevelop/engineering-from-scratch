package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 21 Fixed Verification: Unbounded Stream Iteration Without Limit")
class FixedLab21Test {

    @Test
    @DisplayName("Should verify that FixedLab21 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab21 fixed = new FixedLab21();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
