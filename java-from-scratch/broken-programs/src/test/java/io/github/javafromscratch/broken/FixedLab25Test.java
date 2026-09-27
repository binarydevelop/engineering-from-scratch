package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 25 Fixed Verification: Ternary Operator Hidden Unboxing NPE")
class FixedLab25Test {

    @Test
    @DisplayName("Should verify that FixedLab25 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab25 fixed = new FixedLab25();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
