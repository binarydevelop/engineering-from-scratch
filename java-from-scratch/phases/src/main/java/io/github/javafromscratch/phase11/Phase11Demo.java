package io.github.javafromscratch.phase11;

/**
 * Phase 11: Strings as Immutable Values
 * Motto: Immutability guarantees safe sharing across threads and hash stability.
 */
public class Phase11Demo {
    private final String topic;

    public Phase11Demo() {
        this.topic = "Strings as Immutable Values";
    }

    public String execute() {
        return "Executed " + topic + ": Immutability guarantees safe sharing across threads and hash stability.";
    }

    public static void main(String[] args) {
        Phase11Demo demo = new Phase11Demo();
        System.out.println(demo.execute());
    }
}
