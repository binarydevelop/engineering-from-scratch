package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 141 Test")
class Exercise141Test {

    @Test
    void testSolve() {
        int result = Exercise141.solve(10);
        assertEquals(20 + 141, result);
    }
}
