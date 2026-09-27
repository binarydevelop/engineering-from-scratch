package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 083 Test")
class Exercise083Test {

    @Test
    void testSolve() {
        int result = Exercise083.solve(10);
        assertEquals(20 + 83, result);
    }
}
