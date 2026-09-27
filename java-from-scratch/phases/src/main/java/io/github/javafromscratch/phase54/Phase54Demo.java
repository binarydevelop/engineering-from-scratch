package io.github.javafromscratch.phase54;

/**
 * Phase 54: Checked vs Unchecked Exceptions
 * Motto: Recoverable environmental faults are checked; programmer defects are unchecked.
 */
public class Phase54Demo {
    private final String topic;

    public Phase54Demo() {
        this.topic = "Checked vs Unchecked Exceptions";
    }

    public String execute() {
        return "Executed " + topic + ": Recoverable environmental faults are checked; programmer defects are unchecked.";
    }

    public static void main(String[] args) {
        Phase54Demo demo = new Phase54Demo();
        System.out.println(demo.execute());
    }
}
