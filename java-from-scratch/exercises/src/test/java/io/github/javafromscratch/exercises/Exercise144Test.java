package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 144 Test")
class Exercise144Test {

    @Test
    void testSolve() {
        int result = Exercise144.solve(10);
        assertEquals(20 + 144, result);
    }
}
