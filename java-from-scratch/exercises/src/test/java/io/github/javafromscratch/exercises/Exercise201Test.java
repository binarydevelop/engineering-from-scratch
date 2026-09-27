package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 201 Test")
class Exercise201Test {

    @Test
    void testSolve() {
        int result = Exercise201.solve(10);
        assertEquals(20 + 201, result);
    }
}
