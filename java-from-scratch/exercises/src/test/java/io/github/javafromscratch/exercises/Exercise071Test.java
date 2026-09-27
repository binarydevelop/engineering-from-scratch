package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 071 Test")
class Exercise071Test {

    @Test
    void testSolve() {
        int result = Exercise071.solve(10);
        assertEquals(20 + 71, result);
    }
}
