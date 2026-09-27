package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 028 Test")
class Exercise028Test {

    @Test
    void testSolve() {
        int result = Exercise028.solve(10);
        assertEquals(20 + 28, result);
    }
}
