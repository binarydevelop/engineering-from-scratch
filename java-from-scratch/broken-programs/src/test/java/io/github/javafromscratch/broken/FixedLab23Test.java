package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 23 Fixed Verification: Generics Heap Pollution via Raw Types")
class FixedLab23Test {

    @Test
    @DisplayName("Should verify that FixedLab23 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab23 fixed = new FixedLab23();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
