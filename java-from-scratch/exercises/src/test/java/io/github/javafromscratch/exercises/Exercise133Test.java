package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 133 Test")
class Exercise133Test {

    @Test
    void testSolve() {
        int result = Exercise133.solve(10);
        assertEquals(20 + 133, result);
    }
}
