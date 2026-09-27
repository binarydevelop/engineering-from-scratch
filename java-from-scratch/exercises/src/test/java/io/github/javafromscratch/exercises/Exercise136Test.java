package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 136 Test")
class Exercise136Test {

    @Test
    void testSolve() {
        int result = Exercise136.solve(10);
        assertEquals(20 + 136, result);
    }
}
