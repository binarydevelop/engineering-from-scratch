package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 15 Fixed Verification: Wait Outside Loop and Solitary notify")
class FixedLab15Test {

    @Test
    @DisplayName("Should verify that FixedLab15 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab15 fixed = new FixedLab15();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
