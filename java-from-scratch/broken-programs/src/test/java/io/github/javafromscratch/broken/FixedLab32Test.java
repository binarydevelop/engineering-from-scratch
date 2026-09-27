package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 32 Fixed Verification: LazyInitializationException Outside Session")
class FixedLab32Test {

    @Test
    @DisplayName("Should verify that FixedLab32 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab32 fixed = new FixedLab32();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
