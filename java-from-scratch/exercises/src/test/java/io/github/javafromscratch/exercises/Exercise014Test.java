package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 014 Test")
class Exercise014Test {

    @Test
    void testSolve() {
        int result = Exercise014.solve(10);
        assertEquals(20 + 14, result);
    }
}
