package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 06 Reproduction: GC Allocation Storm from String Concat")
class ReproductionLab06Test {

    @Test
    @DisplayName("Should deterministically reproduce ExcessiveGC")
    void shouldReproduceFailure() {
        BuggyLab06 buggy = new BuggyLab06();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("ExcessiveGC"));
    }
}
