package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 02 Reproduction: ConcurrentModificationException in Loop")
class ReproductionLab02Test {

    @Test
    @DisplayName("Should deterministically reproduce ConcurrentModificationException")
    void shouldReproduceFailure() {
        BuggyLab02 buggy = new BuggyLab02();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("ConcurrentModificationException"));
    }
}
