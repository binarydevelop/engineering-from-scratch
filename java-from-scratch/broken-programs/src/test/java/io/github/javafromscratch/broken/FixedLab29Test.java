package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 29 Fixed Verification: SQL Injection via String Concatenation")
class FixedLab29Test {

    @Test
    @DisplayName("Should verify that FixedLab29 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab29 fixed = new FixedLab29();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
