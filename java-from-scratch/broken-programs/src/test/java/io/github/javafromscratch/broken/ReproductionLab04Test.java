package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 04 Reproduction: Classic Two-Lock Deadlock")
class ReproductionLab04Test {

    @Test
    @DisplayName("Should deterministically reproduce Deadlock")
    void shouldReproduceFailure() {
        BuggyLab04 buggy = new BuggyLab04();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("Deadlock"));
    }
}
