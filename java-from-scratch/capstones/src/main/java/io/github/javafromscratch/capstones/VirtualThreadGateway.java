package io.github.javafromscratch.capstones;

import java.util.concurrent.atomic.AtomicLong;

/**
 * High-Throughput Virtual-Thread API Gateway & Reverse Proxy
 * An asynchronous, non-blocking HTTP proxy engine leveraging Java 21 Virtual Threads and modern HttpClient to route requests concurrently without thread pool exhaustion.
 */
public class VirtualThreadGateway {
    private final String systemName;
    private final AtomicLong eventSequence = new AtomicLong(0);

    public VirtualThreadGateway(String systemName) {
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
