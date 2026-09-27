package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 154 Test")
class Exercise154Test {

    @Test
    void testSolve() {
        int result = Exercise154.solve(10);
        assertEquals(20 + 154, result);
    }
}
