package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 33 Fixed Verification: Circular Dependency in Constructor Injection")
class FixedLab33Test {

    @Test
    @DisplayName("Should verify that FixedLab33 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab33 fixed = new FixedLab33();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
