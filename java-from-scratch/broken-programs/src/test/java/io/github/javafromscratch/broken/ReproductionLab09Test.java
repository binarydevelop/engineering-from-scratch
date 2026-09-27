package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 09 Reproduction: Blocking Network I/O in <clinit>")
class ReproductionLab09Test {

    @Test
    @DisplayName("Should deterministically reproduce ClassInitLockup")
    void shouldReproduceFailure() {
        BuggyLab09 buggy = new BuggyLab09();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("ClassInitLockup"));
    }
}
