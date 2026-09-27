package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 068 Test")
class Exercise068Test {

    @Test
    void testSolve() {
        int result = Exercise068.solve(10);
        assertEquals(20 + 68, result);
    }
}
