package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 062 Test")
class Exercise062Test {

    @Test
    void testSolve() {
        int result = Exercise062.solve(10);
        assertEquals(20 + 62, result);
    }
}
