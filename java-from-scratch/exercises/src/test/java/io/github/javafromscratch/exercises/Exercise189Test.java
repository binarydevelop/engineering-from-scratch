package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 189 Test")
class Exercise189Test {

    @Test
    void testSolve() {
        int result = Exercise189.solve(10);
        assertEquals(20 + 189, result);
    }
}
