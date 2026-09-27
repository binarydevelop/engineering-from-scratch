package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 34 Fixed Verification: Socket Read Hanging Indefinitely Without Timeout")
class FixedLab34Test {

    @Test
    @DisplayName("Should verify that FixedLab34 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab34 fixed = new FixedLab34();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
