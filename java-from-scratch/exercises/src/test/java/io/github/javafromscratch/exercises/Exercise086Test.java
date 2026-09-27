package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 086 Test")
class Exercise086Test {

    @Test
    void testSolve() {
        int result = Exercise086.solve(10);
        assertEquals(20 + 86, result);
    }
}
