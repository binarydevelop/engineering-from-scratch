package io.github.javafromscratch.phase23;

/**
 * Phase 23: Records: Data Carriers
 * Motto: When data is just data, use a record for unambiguous immutability.
 */
public class Phase23Demo {
    private final String topic;

    public Phase23Demo() {
        this.topic = "Records: Data Carriers";
    }

    public String execute() {
        return "Executed " + topic + ": When data is just data, use a record for unambiguous immutability.";
    }

    public static void main(String[] args) {
        Phase23Demo demo = new Phase23Demo();
        System.out.println(demo.execute());
    }
}
