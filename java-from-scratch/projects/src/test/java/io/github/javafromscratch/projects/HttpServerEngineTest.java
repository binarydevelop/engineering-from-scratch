package io.github.javafromscratch.projects;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lightweight HTTP/1.1 Server Test Suite")
class HttpServerEngineTest {

    @Test
    @DisplayName("Should initialize and execute operations reliably")
    void shouldExecuteOperations() {
        HttpServerEngine instance = new HttpServerEngine("Lightweight HTTP/1.1 Server");
        assertEquals("Lightweight HTTP/1.1 Server", instance.getName());
        assertEquals(1, instance.performOperation());
        assertEquals(2, instance.performOperation());
        assertEquals(2, instance.getOperationCount());
    }
}
