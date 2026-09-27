package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 111 Test")
class Exercise111Test {

    @Test
    void testSolve() {
        int result = Exercise111.solve(10);
        assertEquals(20 + 111, result);
    }
}
