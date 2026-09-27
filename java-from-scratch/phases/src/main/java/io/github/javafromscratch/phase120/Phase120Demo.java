package io.github.javafromscratch.phase120;

/**
 * Phase 120: Building a Minimal HTTP Server
 * Motto: An HTTP server is a socket server parsing headers and returning text lines.
 */
public class Phase120Demo {
    private final String topic;

    public Phase120Demo() {
        this.topic = "Building a Minimal HTTP Server";
    }

    public String execute() {
        return "Executed " + topic + ": An HTTP server is a socket server parsing headers and returning text lines.";
    }

    public static void main(String[] args) {
        Phase120Demo demo = new Phase120Demo();
        System.out.println(demo.execute());
    }
}
