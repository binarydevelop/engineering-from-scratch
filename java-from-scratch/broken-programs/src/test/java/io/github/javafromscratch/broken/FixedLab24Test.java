package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 24 Fixed Verification: ArrayStoreException via Covariant Array")
class FixedLab24Test {

    @Test
    @DisplayName("Should verify that FixedLab24 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab24 fixed = new FixedLab24();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
