package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 30 Fixed Verification: Partial Multi-Statement Failure Without Transaction")
class FixedLab30Test {

    @Test
    @DisplayName("Should verify that FixedLab30 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab30 fixed = new FixedLab30();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
