package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 15 Reproduction: Wait Outside Loop and Solitary notify")
class ReproductionLab15Test {

    @Test
    @DisplayName("Should deterministically reproduce LostWakeup")
    void shouldReproduceFailure() {
        BuggyLab15 buggy = new BuggyLab15();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("LostWakeup"));
    }
}
