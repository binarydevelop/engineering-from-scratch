package io.github.javafromscratch.phase113;

/**
 * Phase 113: CountDownLatch & CyclicBarrier
 * Motto: Synchronize thread progress at designated computational checkpoints.
 */
public class Phase113Demo {
    private final String topic;

    public Phase113Demo() {
        this.topic = "CountDownLatch & CyclicBarrier";
    }

    public String execute() {
        return "Executed " + topic + ": Synchronize thread progress at designated computational checkpoints.";
    }

    public static void main(String[] args) {
        Phase113Demo demo = new Phase113Demo();
        System.out.println(demo.execute());
    }
}
