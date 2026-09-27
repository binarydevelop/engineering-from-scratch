package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 040 Test")
class Exercise040Test {

    @Test
    void testSolve() {
        int result = Exercise040.solve(10);
        assertEquals(20 + 40, result);
    }
}
