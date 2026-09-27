package io.github.javafromscratch.phase08;

/**
 * Phase 08: Methods and Stack Execution
 * Motto: A method call is a new activation frame pushed onto the thread stack.
 */
public class Phase08Demo {
    private final String topic;

    public Phase08Demo() {
        this.topic = "Methods and Stack Execution";
    }

    public String execute() {
        return "Executed " + topic + ": A method call is a new activation frame pushed onto the thread stack.";
    }

    public static void main(String[] args) {
        Phase08Demo demo = new Phase08Demo();
        System.out.println(demo.execute());
    }
}
