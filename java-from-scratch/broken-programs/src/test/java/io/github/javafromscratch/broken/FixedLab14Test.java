package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 14 Fixed Verification: Non-Atomic Compound Operation on volatile")
class FixedLab14Test {

    @Test
    @DisplayName("Should verify that FixedLab14 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab14 fixed = new FixedLab14();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
