package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 199 Test")
class Exercise199Test {

    @Test
    void testSolve() {
        int result = Exercise199.solve(10);
        assertEquals(20 + 199, result);
    }
}
