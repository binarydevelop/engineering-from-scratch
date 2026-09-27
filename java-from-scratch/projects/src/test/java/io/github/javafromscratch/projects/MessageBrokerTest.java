package io.github.javafromscratch.projects;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("In-Memory Message Broker Test Suite")
class MessageBrokerTest {

    @Test
    @DisplayName("Should initialize and execute operations reliably")
    void shouldExecuteOperations() {
        MessageBroker instance = new MessageBroker("In-Memory Message Broker");
        assertEquals("In-Memory Message Broker", instance.getName());
        assertEquals(1, instance.performOperation());
        assertEquals(2, instance.performOperation());
        assertEquals(2, instance.getOperationCount());
    }
}
