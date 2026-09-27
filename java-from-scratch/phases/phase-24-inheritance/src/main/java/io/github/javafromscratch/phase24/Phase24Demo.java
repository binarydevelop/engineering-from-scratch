package io.github.javafromscratch.phase24;

/**
 * Phase 24: Inheritance & Subtyping
 * Motto: Inheritance is for 'is-a' substitution, not a code-reuse shortcut.
 */
public class Phase24Demo {
    private final String topic;

    public Phase24Demo() {
        this.topic = "Inheritance & Subtyping";
    }

    public String execute() {
        return "Executed " + topic + ": Inheritance is for 'is-a' substitution, not a code-reuse shortcut.";
    }

    public static void main(String[] args) {
        Phase24Demo demo = new Phase24Demo();
        System.out.println(demo.execute());
    }
}
