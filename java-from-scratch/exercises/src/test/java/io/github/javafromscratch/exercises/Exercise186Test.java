package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 186 Test")
class Exercise186Test {

    @Test
    void testSolve() {
        int result = Exercise186.solve(10);
        assertEquals(20 + 186, result);
    }
}
