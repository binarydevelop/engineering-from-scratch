package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 016 Test")
class Exercise016Test {

    @Test
    void testSolve() {
        int result = Exercise016.solve(10);
        assertEquals(20 + 16, result);
    }
}
