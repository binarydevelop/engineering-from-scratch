package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 28 Fixed Verification: Swallowed Exception in CompletableFuture")
class FixedLab28Test {

    @Test
    @DisplayName("Should verify that FixedLab28 eliminates the failure")
    void shouldVerifyFix() {
        FixedLab28 fixed = new FixedLab28();
        int result = fixed.execute();
        assertEquals(42, result);
    }
}
