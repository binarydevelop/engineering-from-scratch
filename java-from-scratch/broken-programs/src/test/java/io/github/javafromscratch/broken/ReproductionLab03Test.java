package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 03 Reproduction: NoClassDefFoundError After Clinit Failure")
class ReproductionLab03Test {

    @Test
    @DisplayName("Should deterministically reproduce NoClassDefFoundError")
    void shouldReproduceFailure() {
        BuggyLab03 buggy = new BuggyLab03();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("NoClassDefFoundError"));
    }
}
