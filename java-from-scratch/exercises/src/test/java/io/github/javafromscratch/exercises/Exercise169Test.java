package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 169 Test")
class Exercise169Test {

    @Test
    void testSolve() {
        int result = Exercise169.solve(10);
        assertEquals(20 + 169, result);
    }
}
