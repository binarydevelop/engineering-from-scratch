package io.github.javafromscratch.projects;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Resilient Task Runner Test Suite")
class TaskRunnerTest {

    @Test
    @DisplayName("Should initialize and execute operations reliably")
    void shouldExecuteOperations() {
        TaskRunner instance = new TaskRunner("Resilient Task Runner");
        assertEquals("Resilient Task Runner", instance.getName());
        assertEquals(1, instance.performOperation());
        assertEquals(2, instance.performOperation());
        assertEquals(2, instance.getOperationCount());
    }
}
