package io.github.javafromscratch.phase140;

/**
 * Phase 140: Mockito: Usage and Misuse
 * Motto: Mock at architectural boundaries; never mock domain models or simple values.
 */
public class Phase140Demo {
    private final String topic;

    public Phase140Demo() {
        this.topic = "Mockito: Usage and Misuse";
    }

    public String execute() {
        return "Executed " + topic + ": Mock at architectural boundaries; never mock domain models or simple values.";
    }

    public static void main(String[] args) {
        Phase140Demo demo = new Phase140Demo();
        System.out.println(demo.execute());
    }
}
