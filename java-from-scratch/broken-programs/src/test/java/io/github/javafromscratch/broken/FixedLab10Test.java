package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 10 Fixed Verification: Mutable Key Mutates After Put in HashMap")
class FixedLab10Test {

    @Test
    @DisplayName("Should verify that FixedLab10 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab10 fixed = new FixedLab10();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
