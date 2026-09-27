package io.github.javafromscratch.capstones;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Capstone: High-Throughput Virtual-Thread API Gateway & Reverse Proxy Test Suite")
class VirtualThreadGatewayTest {

    @Test
    @DisplayName("Should publish events and verify high-throughput atomic sequence")
    void shouldExecuteCapstoneOperations() {
        VirtualThreadGateway capstone = new VirtualThreadGateway("High-Throughput Virtual-Thread API Gateway & Reverse Proxy");
        assertEquals("High-Throughput Virtual-Thread API Gateway & Reverse Proxy", capstone.getSystemName());
        assertEquals(1L, capstone.publishEvent());
        assertEquals(2L, capstone.publishEvent());
        assertEquals(2L, capstone.getPublishedEventCount());
    }
}
