package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 23 Reproduction: Generics Heap Pollution via Raw Types")
class ReproductionLab23Test {

    @Test
    @DisplayName("Should deterministically reproduce ClassCastException")
    void shouldReproduceFailure() {
        BuggyLab23 buggy = new BuggyLab23();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("ClassCastException"));
    }
}
