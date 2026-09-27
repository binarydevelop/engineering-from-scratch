package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 17 Fixed Verification: Escaping this Reference from Constructor")
class FixedLab17Test {

    @Test
    @DisplayName("Should verify that FixedLab17 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab17 fixed = new FixedLab17();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
