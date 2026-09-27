package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 104 Test")
class Exercise104Test {

    @Test
    void testSolve() {
        int result = Exercise104.solve(10);
        assertEquals(20 + 104, result);
    }
}
