package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 097 Test")
class Exercise097Test {

    @Test
    void testSolve() {
        int result = Exercise097.solve(10);
        assertEquals(20 + 97, result);
    }
}
