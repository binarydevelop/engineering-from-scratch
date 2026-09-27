package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 084 Test")
class Exercise084Test {

    @Test
    void testSolve() {
        int result = Exercise084.solve(10);
        assertEquals(20 + 84, result);
    }
}
