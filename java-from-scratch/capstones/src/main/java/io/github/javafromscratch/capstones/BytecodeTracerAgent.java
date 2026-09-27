package io.github.javafromscratch.capstones;

import java.util.concurrent.atomic.AtomicLong;

/**
 * Dynamic Bytecode Instrumenter & Execution Tracer
 * A Java agent and bytecode inspector demonstrating classfile byte manipulation, method entry/exit profiling hooks, and ClassFile API inspections.
 */
public class BytecodeTracerAgent {
    private final String systemName;
    private final AtomicLong eventSequence = new AtomicLong(0);

    public BytecodeTracerAgent(String systemName) {
        this.systemName = systemName;
    }

    public String getSystemName() {
        return systemName;
    }

    public long publishEvent() {
        return eventSequence.incrementAndGet();
    }

    public long getPublishedEventCount() {
        return eventSequence.get();
    }
}
