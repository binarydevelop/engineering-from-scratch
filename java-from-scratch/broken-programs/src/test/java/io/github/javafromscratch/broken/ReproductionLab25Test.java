package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 25 Reproduction: Ternary Operator Hidden Unboxing NPE")
class ReproductionLab25Test {

    @Test
    @DisplayName("Should deterministically reproduce NullPointerException")
    void shouldReproduceFailure() {
        BuggyLab25 buggy = new BuggyLab25();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("NullPointerException"));
    }
}
