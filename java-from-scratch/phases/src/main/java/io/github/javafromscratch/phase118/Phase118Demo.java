package io.github.javafromscratch.phase118;

/**
 * Phase 118: TCP Sockets from Scratch
 * Motto: Network programming is reading and writing byte streams over OS sockets.
 */
public class Phase118Demo {
    private final String topic;

    public Phase118Demo() {
        this.topic = "TCP Sockets from Scratch";
    }

    public String execute() {
        return "Executed " + topic + ": Network programming is reading and writing byte streams over OS sockets.";
    }

    public static void main(String[] args) {
        Phase118Demo demo = new Phase118Demo();
        System.out.println(demo.execute());
    }
}
