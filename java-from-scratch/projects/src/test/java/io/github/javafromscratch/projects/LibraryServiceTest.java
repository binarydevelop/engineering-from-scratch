package io.github.javafromscratch.projects;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Library Management System Test Suite")
class LibraryServiceTest {

    @Test
    @DisplayName("Should initialize and execute operations reliably")
    void shouldExecuteOperations() {
        LibraryService instance = new LibraryService("Library Management System");
        assertEquals("Library Management System", instance.getName());
        assertEquals(1, instance.performOperation());
        assertEquals(2, instance.performOperation());
        assertEquals(2, instance.getOperationCount());
    }
}
