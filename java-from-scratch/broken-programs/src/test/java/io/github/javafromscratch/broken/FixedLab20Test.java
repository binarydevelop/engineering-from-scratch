package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 20 Fixed Verification: Financial Arithmetic Error with double")
class FixedLab20Test {

    @Test
    @DisplayName("Should verify that FixedLab20 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab20 fixed = new FixedLab20();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
