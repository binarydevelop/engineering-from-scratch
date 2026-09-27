package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 150 Test")
class Exercise150Test {

    @Test
    void testSolve() {
        int result = Exercise150.solve(10);
        assertEquals(20 + 150, result);
    }
}
