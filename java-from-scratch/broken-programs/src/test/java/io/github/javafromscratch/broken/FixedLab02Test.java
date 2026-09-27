package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 02 Fixed Verification: ConcurrentModificationException in Loop")
class FixedLab02Test {

    @Test
    @DisplayName("Should verify that FixedLab02 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab02 fixed = new FixedLab02();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
