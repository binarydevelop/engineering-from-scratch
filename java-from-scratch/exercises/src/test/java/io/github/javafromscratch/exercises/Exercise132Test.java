package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 132 Test")
class Exercise132Test {

    @Test
    void testSolve() {
        int result = Exercise132.solve(10);
        assertEquals(20 + 132, result);
    }
}
