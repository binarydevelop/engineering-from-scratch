package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 13 Reproduction: Infinite Loop Due to Lack of volatile")
class ReproductionLab13Test {

    @Test
    @DisplayName("Should deterministically reproduce VisibilityFailure")
    void shouldReproduceFailure() {
        BuggyLab13 buggy = new BuggyLab13();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("VisibilityFailure"));
    }
}
