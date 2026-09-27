package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 03 Fixed Verification: NoClassDefFoundError After Clinit Failure")
class FixedLab03Test {

    @Test
    @DisplayName("Should verify that FixedLab03 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab03 fixed = new FixedLab03();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
