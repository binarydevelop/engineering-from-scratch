package io.github.javafromscratch.phase65;

/**
 * Phase 65: Precision Money with BigDecimal
 * Motto: Never represent monetary currency with floating-point types.
 */
public class Phase65Demo {
    private final String topic;

    public Phase65Demo() {
        this.topic = "Precision Money with BigDecimal";
    }

    public String execute() {
        return "Executed " + topic + ": Never represent monetary currency with floating-point types.";
    }

    public static void main(String[] args) {
        Phase65Demo demo = new Phase65Demo();
        System.out.println(demo.execute());
    }
}
