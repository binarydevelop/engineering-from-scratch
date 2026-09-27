package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 11 Reproduction: equals Implemented Without hashCode")
class ReproductionLab11Test {

    @Test
    @DisplayName("Should deterministically reproduce SetCorruption")
    void shouldReproduceFailure() {
        BuggyLab11 buggy = new BuggyLab11();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("SetCorruption"));
    }
}
