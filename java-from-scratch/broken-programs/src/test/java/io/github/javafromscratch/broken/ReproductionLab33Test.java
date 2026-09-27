package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 33 Reproduction: Circular Dependency in Constructor Injection")
class ReproductionLab33Test {

    @Test
    @DisplayName("Should deterministically reproduce StackOverflowError")
    void shouldReproduceFailure() {
        BuggyLab33 buggy = new BuggyLab33();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("StackOverflowError"));
    }
}
