package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 146 Test")
class Exercise146Test {

    @Test
    void testSolve() {
        int result = Exercise146.solve(10);
        assertEquals(20 + 146, result);
    }
}
