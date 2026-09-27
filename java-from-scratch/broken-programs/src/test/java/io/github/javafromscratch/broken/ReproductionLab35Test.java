package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 35 Reproduction: StackOverflowError from Unbounded Recursion")
class ReproductionLab35Test {

    @Test
    @DisplayName("Should deterministically reproduce StackOverflowError")
    void shouldReproduceFailure() {
        BuggyLab35 buggy = new BuggyLab35();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("StackOverflowError"));
    }
}
