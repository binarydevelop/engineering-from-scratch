package io.github.javafromscratch.phase50;

/**
 * Phase 50: Generics Subtyping and Wildcards
 * Motto: List<Integer> is NOT a subtype of List<Number>.
 */
public class Phase50Demo {
    private final String topic;

    public Phase50Demo() {
        this.topic = "Generics Subtyping and Wildcards";
    }

    public String execute() {
        return "Executed " + topic + ": List<Integer> is NOT a subtype of List<Number>.";
    }

    public static void main(String[] args) {
        Phase50Demo demo = new Phase50Demo();
        System.out.println(demo.execute());
    }
}
