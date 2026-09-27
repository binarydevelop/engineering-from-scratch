package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 020 Test")
class Exercise020Test {

    @Test
    void testSolve() {
        int result = Exercise020.solve(10);
        assertEquals(20 + 20, result);
    }
}
