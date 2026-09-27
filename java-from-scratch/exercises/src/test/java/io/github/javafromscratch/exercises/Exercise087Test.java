package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 087 Test")
class Exercise087Test {

    @Test
    void testSolve() {
        int result = Exercise087.solve(10);
        assertEquals(20 + 87, result);
    }
}
