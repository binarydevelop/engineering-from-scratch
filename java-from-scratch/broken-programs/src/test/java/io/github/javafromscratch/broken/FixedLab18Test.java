package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 18 Fixed Verification: Unclosed FileInputStream Leaking OS Handles")
class FixedLab18Test {

    @Test
    @DisplayName("Should verify that FixedLab18 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab18 fixed = new FixedLab18();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
