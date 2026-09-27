package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 34 Reproduction: Socket Read Hanging Indefinitely Without Timeout")
class ReproductionLab34Test {

    @Test
    @DisplayName("Should deterministically reproduce SocketHang")
    void shouldReproduceFailure() {
        BuggyLab34 buggy = new BuggyLab34();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("SocketHang"));
    }
}
