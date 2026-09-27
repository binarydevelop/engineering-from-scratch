package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 003 Test")
class Exercise003Test {

    @Test
    void testSolve() {
        int result = Exercise003.solve(10);
        assertEquals(20 + 3, result);
    }
}
