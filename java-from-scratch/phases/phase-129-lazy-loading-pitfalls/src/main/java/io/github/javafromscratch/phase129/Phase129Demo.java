package io.github.javafromscratch.phase129;

/**
 * Phase 129: Lazy Loading & Detached Entities
 * Motto: Accessing lazy properties outside an active transaction throws LazyInitializationException.
 */
public class Phase129Demo {
    private final String topic;

    public Phase129Demo() {
        this.topic = "Lazy Loading & Detached Entities";
    }

    public String execute() {
        return "Executed " + topic + ": Accessing lazy properties outside an active transaction throws LazyInitializationException.";
    }

    public static void main(String[] args) {
        Phase129Demo demo = new Phase129Demo();
        System.out.println(demo.execute());
    }
}
