package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 102 Test")
class Exercise102Test {

    @Test
    void testSolve() {
        int result = Exercise102.solve(10);
        assertEquals(20 + 102, result);
    }
}
