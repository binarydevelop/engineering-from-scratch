package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 017 Test")
class Exercise017Test {

    @Test
    void testSolve() {
        int result = Exercise017.solve(10);
        assertEquals(20 + 17, result);
    }
}
