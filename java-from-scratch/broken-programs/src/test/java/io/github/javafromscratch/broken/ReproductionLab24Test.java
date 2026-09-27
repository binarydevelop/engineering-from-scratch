package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 24 Reproduction: ArrayStoreException via Covariant Array")
class ReproductionLab24Test {

    @Test
    @DisplayName("Should deterministically reproduce ArrayStoreException")
    void shouldReproduceFailure() {
        BuggyLab24 buggy = new BuggyLab24();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("ArrayStoreException"));
    }
}
