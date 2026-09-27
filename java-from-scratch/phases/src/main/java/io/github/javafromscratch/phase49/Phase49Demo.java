package io.github.javafromscratch.phase49;

/**
 * Phase 49: Bounded Type Parameters
 * Motto: Bounds restrict type parameters to types that support required capabilities.
 */
public class Phase49Demo {
    private final String topic;

    public Phase49Demo() {
        this.topic = "Bounded Type Parameters";
    }

    public String execute() {
        return "Executed " + topic + ": Bounds restrict type parameters to types that support required capabilities.";
    }

    public static void main(String[] args) {
        Phase49Demo demo = new Phase49Demo();
        System.out.println(demo.execute());
    }
}
