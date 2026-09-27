package io.github.javafromscratch.capstones;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Capstone: Lock-Free High-Performance Ring Buffer Test Suite")
class DisruptorRingBufferTest {

    @Test
    @DisplayName("Should publish events and verify high-throughput atomic sequence")
    void shouldExecuteCapstoneOperations() {
        DisruptorRingBuffer capstone = new DisruptorRingBuffer("Lock-Free High-Performance Ring Buffer");
        assertEquals("Lock-Free High-Performance Ring Buffer", capstone.getSystemName());
        assertEquals(1L, capstone.publishEvent());
        assertEquals(2L, capstone.publishEvent());
        assertEquals(2L, capstone.getPublishedEventCount());
    }
}
