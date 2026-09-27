package io.github.javafromscratch.phase176;

/**
 * Phase 176: Project 6: Lightweight HTTP Server
 * Motto: Build an HTTP/1.1 server from raw TCP sockets with virtual threads.
 */
public class Phase176Demo {
    private final String topic;

    public Phase176Demo() {
        this.topic = "Project 6: Lightweight HTTP Server";
    }

    public String execute() {
        return "Executed " + topic + ": Build an HTTP/1.1 server from raw TCP sockets with virtual threads.";
    }

    public static void main(String[] args) {
        Phase176Demo demo = new Phase176Demo();
        System.out.println(demo.execute());
    }
}
