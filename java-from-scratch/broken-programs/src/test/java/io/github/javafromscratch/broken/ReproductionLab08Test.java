package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 08 Reproduction: Leaked Database Connection")
class ReproductionLab08Test {

    @Test
    @DisplayName("Should deterministically reproduce PoolExhaustion")
    void shouldReproduceFailure() {
        BuggyLab08 buggy = new BuggyLab08();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("PoolExhaustion"));
    }
}
