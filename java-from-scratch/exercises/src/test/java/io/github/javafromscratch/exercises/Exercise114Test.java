package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 114 Test")
class Exercise114Test {

    @Test
    void testSolve() {
        int result = Exercise114.solve(10);
        assertEquals(20 + 114, result);
    }
}
