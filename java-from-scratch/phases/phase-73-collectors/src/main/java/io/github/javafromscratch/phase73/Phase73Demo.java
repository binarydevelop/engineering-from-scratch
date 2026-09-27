package io.github.javafromscratch.phase73;

/**
 * Phase 73: Collectors & Reductions
 * Motto: Collectors fold stream elements into complex downstream data structures.
 */
public class Phase73Demo {
    private final String topic;

    public Phase73Demo() {
        this.topic = "Collectors & Reductions";
    }

    public String execute() {
        return "Executed " + topic + ": Collectors fold stream elements into complex downstream data structures.";
    }

    public static void main(String[] args) {
        Phase73Demo demo = new Phase73Demo();
        System.out.println(demo.execute());
    }
}
