package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 055 Test")
class Exercise055Test {

    @Test
    void testSolve() {
        int result = Exercise055.solve(10);
        assertEquals(20 + 55, result);
    }
}
