package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 09 Fixed Verification: Blocking Network I/O in <clinit>")
class FixedLab09Test {

    @Test
    @DisplayName("Should verify that FixedLab09 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab09 fixed = new FixedLab09();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
