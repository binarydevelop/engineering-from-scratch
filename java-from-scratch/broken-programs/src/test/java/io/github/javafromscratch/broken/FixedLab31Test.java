package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 31 Fixed Verification: N+1 Database Query Avalanche")
class FixedLab31Test {

    @Test
    @DisplayName("Should verify that FixedLab31 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab31 fixed = new FixedLab31();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
