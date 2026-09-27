package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 142 Test")
class Exercise142Test {

    @Test
    void testSolve() {
        int result = Exercise142.solve(10);
        assertEquals(20 + 142, result);
    }
}
