package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 157 Test")
class Exercise157Test {

    @Test
    void testSolve() {
        int result = Exercise157.solve(10);
        assertEquals(20 + 157, result);
    }
}
