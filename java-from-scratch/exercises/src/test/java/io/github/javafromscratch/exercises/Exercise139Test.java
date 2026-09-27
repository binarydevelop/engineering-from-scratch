package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 139 Test")
class Exercise139Test {

    @Test
    void testSolve() {
        int result = Exercise139.solve(10);
        assertEquals(20 + 139, result);
    }
}
