package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 19 Reproduction: Character Encoding Corruption on Byte Conversions")
class ReproductionLab19Test {

    @Test
    @DisplayName("Should deterministically reproduce EncodingMismatch")
    void shouldReproduceFailure() {
        BuggyLab19 buggy = new BuggyLab19();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("EncodingMismatch"));
    }
}
