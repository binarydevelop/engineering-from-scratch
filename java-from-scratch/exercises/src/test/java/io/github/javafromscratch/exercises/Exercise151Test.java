package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 151 Test")
class Exercise151Test {

    @Test
    void testSolve() {
        int result = Exercise151.solve(10);
        assertEquals(20 + 151, result);
    }
}
