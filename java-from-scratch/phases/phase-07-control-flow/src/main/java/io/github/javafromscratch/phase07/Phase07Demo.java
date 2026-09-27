package io.github.javafromscratch.phase07;

/**
 * Phase 07: Control Flow & Pattern Matching
 * Motto: Control flow translates to conditional jumps in the operand stack.
 */
public class Phase07Demo {
    private final String topic;

    public Phase07Demo() {
        this.topic = "Control Flow & Pattern Matching";
    }

    public String execute() {
        return "Executed " + topic + ": Control flow translates to conditional jumps in the operand stack.";
    }

    public static void main(String[] args) {
        Phase07Demo demo = new Phase07Demo();
        System.out.println(demo.execute());
    }
}
