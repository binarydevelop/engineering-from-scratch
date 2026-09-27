package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 085 Test")
class Exercise085Test {

    @Test
    void testSolve() {
        int result = Exercise085.solve(10);
        assertEquals(20 + 85, result);
    }
}
