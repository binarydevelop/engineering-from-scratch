package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 130 Test")
class Exercise130Test {

    @Test
    void testSolve() {
        int result = Exercise130.solve(10);
        assertEquals(20 + 130, result);
    }
}
