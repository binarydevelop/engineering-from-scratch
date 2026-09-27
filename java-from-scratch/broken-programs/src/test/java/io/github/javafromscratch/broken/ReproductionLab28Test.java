package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 28 Reproduction: Swallowed Exception in CompletableFuture")
class ReproductionLab28Test {

    @Test
    @DisplayName("Should deterministically reproduce SilentFailure")
    void shouldReproduceFailure() {
        BuggyLab28 buggy = new BuggyLab28();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("SilentFailure"));
    }
}
