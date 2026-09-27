package io.github.javafromscratch.phase67;

/**
 * Phase 67: Lambdas: Anonymous Functions
 * Motto: A lambda is code treated as data, desugared into invokedynamic calls.
 */
public class Phase67Demo {
    private final String topic;

    public Phase67Demo() {
        this.topic = "Lambdas: Anonymous Functions";
    }

    public String execute() {
        return "Executed " + topic + ": A lambda is code treated as data, desugared into invokedynamic calls.";
    }

    public static void main(String[] args) {
        Phase67Demo demo = new Phase67Demo();
        System.out.println(demo.execute());
    }
}
