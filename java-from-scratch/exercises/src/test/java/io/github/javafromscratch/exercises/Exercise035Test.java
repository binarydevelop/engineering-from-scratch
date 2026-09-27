package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 035 Test")
class Exercise035Test {

    @Test
    void testSolve() {
        int result = Exercise035.solve(10);
        assertEquals(20 + 35, result);
    }
}
