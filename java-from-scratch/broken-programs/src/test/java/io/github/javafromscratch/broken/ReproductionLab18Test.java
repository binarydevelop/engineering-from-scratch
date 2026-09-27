package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 18 Reproduction: Unclosed FileInputStream Leaking OS Handles")
class ReproductionLab18Test {

    @Test
    @DisplayName("Should deterministically reproduce DescriptorLeak")
    void shouldReproduceFailure() {
        BuggyLab18 buggy = new BuggyLab18();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("DescriptorLeak"));
    }
}
