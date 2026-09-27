package io.github.javafromscratch.phase80;

/**
 * Phase 80: Stack Frames & Operand Stack
 * Motto: JVM execution is a stack of frames containing local variables and operand stacks.
 */
public class Phase80Demo {
    private final String topic;

    public Phase80Demo() {
        this.topic = "Stack Frames & Operand Stack";
    }

    public String execute() {
        return "Executed " + topic + ": JVM execution is a stack of frames containing local variables and operand stacks.";
    }

    public static void main(String[] args) {
        Phase80Demo demo = new Phase80Demo();
        System.out.println(demo.execute());
    }
}
