package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 21 Reproduction: Unbounded Stream Iteration Without Limit")
class ReproductionLab21Test {

    @Test
    @DisplayName("Should deterministically reproduce HeapExhaustion")
    void shouldReproduceFailure() {
        BuggyLab21 buggy = new BuggyLab21();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("HeapExhaustion"));
    }
}
