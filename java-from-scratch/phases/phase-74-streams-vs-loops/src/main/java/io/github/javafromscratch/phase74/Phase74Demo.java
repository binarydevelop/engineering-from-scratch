package io.github.javafromscratch.phase74;

/**
 * Phase 74: Streams vs Loops Performance
 * Motto: Write for humans first; optimize with loops only when profiling proves necessary.
 */
public class Phase74Demo {
    private final String topic;

    public Phase74Demo() {
        this.topic = "Streams vs Loops Performance";
    }

    public String execute() {
        return "Executed " + topic + ": Write for humans first; optimize with loops only when profiling proves necessary.";
    }

    public static void main(String[] args) {
        Phase74Demo demo = new Phase74Demo();
        System.out.println(demo.execute());
    }
}
