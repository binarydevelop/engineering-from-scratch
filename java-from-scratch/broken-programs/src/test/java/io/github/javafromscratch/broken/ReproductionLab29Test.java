package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 29 Reproduction: SQL Injection via String Concatenation")
class ReproductionLab29Test {

    @Test
    @DisplayName("Should deterministically reproduce SecurityBreach")
    void shouldReproduceFailure() {
        BuggyLab29 buggy = new BuggyLab29();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("SecurityBreach"));
    }
}
