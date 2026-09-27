package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 029 Test")
class Exercise029Test {

    @Test
    void testSolve() {
        int result = Exercise029.solve(10);
        assertEquals(20 + 29, result);
    }
}
