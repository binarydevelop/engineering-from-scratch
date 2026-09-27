package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 027 Test")
class Exercise027Test {

    @Test
    void testSolve() {
        int result = Exercise027.solve(10);
        assertEquals(20 + 27, result);
    }
}
