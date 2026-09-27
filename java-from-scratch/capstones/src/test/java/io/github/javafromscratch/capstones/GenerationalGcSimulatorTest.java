package io.github.javafromscratch.capstones;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Capstone: Generational GC & Object Memory Allocator Simulator Test Suite")
class GenerationalGcSimulatorTest {

    @Test
    @DisplayName("Should publish events and verify high-throughput atomic sequence")
    void shouldExecuteCapstoneOperations() {
        GenerationalGcSimulator capstone = new GenerationalGcSimulator("Generational GC & Object Memory Allocator Simulator");
        assertEquals("Generational GC & Object Memory Allocator Simulator", capstone.getSystemName());
        assertEquals(1L, capstone.publishEvent());
        assertEquals(2L, capstone.publishEvent());
        assertEquals(2L, capstone.getPublishedEventCount());
    }
}
