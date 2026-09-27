package io.github.javafromscratch.phase101;

/**
 * Phase 101: Deadlocks: Creation & Prevention
 * Motto: Deadlock occurs when circular lock acquisition dependencies form.
 */
public class Phase101Demo {
    private final String topic;

    public Phase101Demo() {
        this.topic = "Deadlocks: Creation & Prevention";
    }

    public String execute() {
        return "Executed " + topic + ": Deadlock occurs when circular lock acquisition dependencies form.";
    }

    public static void main(String[] args) {
        Phase101Demo demo = new Phase101Demo();
        System.out.println(demo.execute());
    }
}
