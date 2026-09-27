package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 198 Test")
class Exercise198Test {

    @Test
    void testSolve() {
        int result = Exercise198.solve(10);
        assertEquals(20 + 198, result);
    }
}
