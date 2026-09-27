package io.github.javafromscratch.phase152;

/**
 * Phase 152: Allocation Profiling & GC Pressure
 * Motto: The fastest garbage collection is the one that never has to run.
 */
public class Phase152Demo {
    private final String topic;

    public Phase152Demo() {
        this.topic = "Allocation Profiling & GC Pressure";
    }

    public String execute() {
        return "Executed " + topic + ": The fastest garbage collection is the one that never has to run.";
    }

    public static void main(String[] args) {
        Phase152Demo demo = new Phase152Demo();
        System.out.println(demo.execute());
    }
}
