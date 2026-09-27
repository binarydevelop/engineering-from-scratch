package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 11 Fixed Verification: equals Implemented Without hashCode")
class FixedLab11Test {

    @Test
    @DisplayName("Should verify that FixedLab11 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab11 fixed = new FixedLab11();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
