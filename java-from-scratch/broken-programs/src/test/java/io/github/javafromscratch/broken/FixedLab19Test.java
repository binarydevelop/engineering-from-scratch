package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 19 Fixed Verification: Character Encoding Corruption on Byte Conversions")
class FixedLab19Test {

    @Test
    @DisplayName("Should verify that FixedLab19 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab19 fixed = new FixedLab19();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
