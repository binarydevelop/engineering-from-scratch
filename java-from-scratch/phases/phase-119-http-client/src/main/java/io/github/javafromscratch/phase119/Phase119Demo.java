package io.github.javafromscratch.phase119;

/**
 * Phase 119: Modern HTTP Client (java.net.http)
 * Motto: Issue resilient HTTP requests with modern asynchronous HTTP clients.
 */
public class Phase119Demo {
    private final String topic;

    public Phase119Demo() {
        this.topic = "Modern HTTP Client (java.net.http)";
    }

    public String execute() {
        return "Executed " + topic + ": Issue resilient HTTP requests with modern asynchronous HTTP clients.";
    }

    public static void main(String[] args) {
        Phase119Demo demo = new Phase119Demo();
        System.out.println(demo.execute());
    }
}
