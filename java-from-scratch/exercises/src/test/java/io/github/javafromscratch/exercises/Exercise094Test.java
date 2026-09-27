package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 094 Test")
class Exercise094Test {

    @Test
    void testSolve() {
        int result = Exercise094.solve(10);
        assertEquals(20 + 94, result);
    }
}
