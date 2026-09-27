package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 32 Reproduction: LazyInitializationException Outside Session")
class ReproductionLab32Test {

    @Test
    @DisplayName("Should deterministically reproduce LazyInitializationException")
    void shouldReproduceFailure() {
        BuggyLab32 buggy = new BuggyLab32();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("LazyInitializationException"));
    }
}
