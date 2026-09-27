package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 042 Test")
class Exercise042Test {

    @Test
    void testSolve() {
        int result = Exercise042.solve(10);
        assertEquals(20 + 42, result);
    }
}
