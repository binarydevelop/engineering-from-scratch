package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 13 Fixed Verification: Infinite Loop Due to Lack of volatile")
class FixedLab13Test {

    @Test
    @DisplayName("Should verify that FixedLab13 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab13 fixed = new FixedLab13();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
