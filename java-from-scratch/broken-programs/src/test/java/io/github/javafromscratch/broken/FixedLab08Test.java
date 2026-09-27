package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 08 Fixed Verification: Leaked Database Connection")
class FixedLab08Test {

    @Test
    @DisplayName("Should verify that FixedLab08 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab08 fixed = new FixedLab08();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
