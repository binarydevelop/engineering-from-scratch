package io.github.javafromscratch.phase104;

/**
 * Phase 104: Bounded Buffers: BlockingQueue
 * Motto: BlockingQueue encapsulates thread coordination into safe put and take semantics.
 */
public class Phase104Demo {
    private final String topic;

    public Phase104Demo() {
        this.topic = "Bounded Buffers: BlockingQueue";
    }

    public String execute() {
        return "Executed " + topic + ": BlockingQueue encapsulates thread coordination into safe put and take semantics.";
    }

    public static void main(String[] args) {
        Phase104Demo demo = new Phase104Demo();
        System.out.println(demo.execute());
    }
}
