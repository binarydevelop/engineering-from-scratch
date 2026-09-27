package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 122 Test")
class Exercise122Test {

    @Test
    void testSolve() {
        int result = Exercise122.solve(10);
        assertEquals(20 + 122, result);
    }
}
