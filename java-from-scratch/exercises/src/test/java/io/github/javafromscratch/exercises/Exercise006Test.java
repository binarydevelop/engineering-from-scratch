package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 006 Test")
class Exercise006Test {

    @Test
    void testSolve() {
        int result = Exercise006.solve(10);
        assertEquals(20 + 6, result);
    }
}
