package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 092 Test")
class Exercise092Test {

    @Test
    void testSolve() {
        int result = Exercise092.solve(10);
        assertEquals(20 + 92, result);
    }
}
