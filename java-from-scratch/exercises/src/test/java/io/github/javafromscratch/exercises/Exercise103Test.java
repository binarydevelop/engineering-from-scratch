package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 103 Test")
class Exercise103Test {

    @Test
    void testSolve() {
        int result = Exercise103.solve(10);
        assertEquals(20 + 103, result);
    }
}
