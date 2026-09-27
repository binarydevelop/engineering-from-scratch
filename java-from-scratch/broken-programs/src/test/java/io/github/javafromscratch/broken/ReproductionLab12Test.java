package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 12 Reproduction: Race Condition on Non-Synchronized Shared Counter")
class ReproductionLab12Test {

    @Test
    @DisplayName("Should deterministically reproduce LostUpdates")
    void shouldReproduceFailure() {
        BuggyLab12 buggy = new BuggyLab12();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("LostUpdates"));
    }
}
