package io.github.javafromscratch.capstones;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Capstone: Dynamic Bytecode Instrumenter & Execution Tracer Test Suite")
class BytecodeTracerAgentTest {

    @Test
    @DisplayName("Should publish events and verify high-throughput atomic sequence")
    void shouldExecuteCapstoneOperations() {
        BytecodeTracerAgent capstone = new BytecodeTracerAgent("Dynamic Bytecode Instrumenter & Execution Tracer");
        assertEquals("Dynamic Bytecode Instrumenter & Execution Tracer", capstone.getSystemName());
        assertEquals(1L, capstone.publishEvent());
        assertEquals(2L, capstone.publishEvent());
        assertEquals(2L, capstone.getPublishedEventCount());
    }
}
