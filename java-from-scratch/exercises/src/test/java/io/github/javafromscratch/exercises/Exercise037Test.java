package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 037 Test")
class Exercise037Test {

    @Test
    void testSolve() {
        int result = Exercise037.solve(10);
        assertEquals(20 + 37, result);
    }
}
