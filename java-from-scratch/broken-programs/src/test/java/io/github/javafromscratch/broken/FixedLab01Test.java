package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 01 Fixed Verification: Hidden NullPointerException in Chained Call")
class FixedLab01Test {

    @Test
    @DisplayName("Should verify that FixedLab01 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab01 fixed = new FixedLab01();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
