package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 021 Test")
class Exercise021Test {

    @Test
    void testSolve() {
        int result = Exercise021.solve(10);
        assertEquals(20 + 21, result);
    }
}
