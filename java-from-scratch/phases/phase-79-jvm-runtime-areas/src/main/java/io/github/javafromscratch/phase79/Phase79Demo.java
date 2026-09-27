package io.github.javafromscratch.phase79;

/**
 * Phase 79: JVM Runtime Memory Areas
 * Motto: Understand every byte allocated in the JVM process address space.
 */
public class Phase79Demo {
    private final String topic;

    public Phase79Demo() {
        this.topic = "JVM Runtime Memory Areas";
    }

    public String execute() {
        return "Executed " + topic + ": Understand every byte allocated in the JVM process address space.";
    }

    public static void main(String[] args) {
        Phase79Demo demo = new Phase79Demo();
        System.out.println(demo.execute());
    }
}
