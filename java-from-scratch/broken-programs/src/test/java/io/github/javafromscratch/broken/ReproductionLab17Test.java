package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 17 Reproduction: Escaping this Reference from Constructor")
class ReproductionLab17Test {

    @Test
    @DisplayName("Should deterministically reproduce PartiallyInitialized")
    void shouldReproduceFailure() {
        BuggyLab17 buggy = new BuggyLab17();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("PartiallyInitialized"));
    }
}
