package io.github.javafromscratch.phase69;

/**
 * Phase 69: Method References
 * Motto: Method references make existing methods first-class functional values.
 */
public class Phase69Demo {
    private final String topic;

    public Phase69Demo() {
        this.topic = "Method References";
    }

    public String execute() {
        return "Executed " + topic + ": Method references make existing methods first-class functional values.";
    }

    public static void main(String[] args) {
        Phase69Demo demo = new Phase69Demo();
        System.out.println(demo.execute());
    }
}
