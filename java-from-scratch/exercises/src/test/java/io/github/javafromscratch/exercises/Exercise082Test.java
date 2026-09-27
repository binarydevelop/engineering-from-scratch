package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 082 Test")
class Exercise082Test {

    @Test
    void testSolve() {
        int result = Exercise082.solve(10);
        assertEquals(20 + 82, result);
    }
}
