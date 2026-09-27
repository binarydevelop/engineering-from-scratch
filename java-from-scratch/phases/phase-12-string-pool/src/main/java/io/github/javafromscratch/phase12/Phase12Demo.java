package io.github.javafromscratch.phase12;

/**
 * Phase 12: The String Constant Pool
 * Motto: The string pool is a JVM intern table deduplicating literal strings.
 */
public class Phase12Demo {
    private final String topic;

    public Phase12Demo() {
        this.topic = "The String Constant Pool";
    }

    public String execute() {
        return "Executed " + topic + ": The string pool is a JVM intern table deduplicating literal strings.";
    }

    public static void main(String[] args) {
        Phase12Demo demo = new Phase12Demo();
        System.out.println(demo.execute());
    }
}
