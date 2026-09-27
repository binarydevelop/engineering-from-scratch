package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 063 Test")
class Exercise063Test {

    @Test
    void testSolve() {
        int result = Exercise063.solve(10);
        assertEquals(20 + 63, result);
    }
}
