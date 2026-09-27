package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 04 Fixed Verification: Classic Two-Lock Deadlock")
class FixedLab04Test {

    @Test
    @DisplayName("Should verify that FixedLab04 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab04 fixed = new FixedLab04();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
