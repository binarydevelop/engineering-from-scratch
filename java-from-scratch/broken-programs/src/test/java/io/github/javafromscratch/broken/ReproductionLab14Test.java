package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 14 Reproduction: Non-Atomic Compound Operation on volatile")
class ReproductionLab14Test {

    @Test
    @DisplayName("Should deterministically reproduce LostUpdates")
    void shouldReproduceFailure() {
        BuggyLab14 buggy = new BuggyLab14();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("LostUpdates"));
    }
}
