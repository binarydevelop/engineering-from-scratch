package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 187 Test")
class Exercise187Test {

    @Test
    void testSolve() {
        int result = Exercise187.solve(10);
        assertEquals(20 + 187, result);
    }
}
