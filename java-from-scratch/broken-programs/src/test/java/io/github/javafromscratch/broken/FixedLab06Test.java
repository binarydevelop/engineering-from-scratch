package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 06 Fixed Verification: GC Allocation Storm from String Concat")
class FixedLab06Test {

    @Test
    @DisplayName("Should verify that FixedLab06 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab06 fixed = new FixedLab06();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
