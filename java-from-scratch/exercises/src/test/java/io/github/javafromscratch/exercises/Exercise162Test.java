package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 162 Test")
class Exercise162Test {

    @Test
    void testSolve() {
        int result = Exercise162.solve(10);
        assertEquals(20 + 162, result);
    }
}
