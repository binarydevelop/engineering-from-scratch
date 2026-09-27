package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 12 Fixed Verification: Race Condition on Non-Synchronized Shared Counter")
class FixedLab12Test {

    @Test
    @DisplayName("Should verify that FixedLab12 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab12 fixed = new FixedLab12();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
