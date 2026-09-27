package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 196 Test")
class Exercise196Test {

    @Test
    void testSolve() {
        int result = Exercise196.solve(10);
        assertEquals(20 + 196, result);
    }
}
