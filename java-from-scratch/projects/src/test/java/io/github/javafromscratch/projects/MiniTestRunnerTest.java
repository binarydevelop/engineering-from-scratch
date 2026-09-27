package io.github.javafromscratch.projects;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Mini Test Discovery & Runner Test Suite")
class MiniTestRunnerTest {

    @Test
    @DisplayName("Should initialize and execute operations reliably")
    void shouldExecuteOperations() {
        MiniTestRunner instance = new MiniTestRunner("Mini Test Discovery & Runner");
        assertEquals("Mini Test Discovery & Runner", instance.getName());
        assertEquals(1, instance.performOperation());
        assertEquals(2, instance.performOperation());
        assertEquals(2, instance.getOperationCount());
    }
}
