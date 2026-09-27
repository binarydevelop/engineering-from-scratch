package io.github.javafromscratch.phase01;

/**
 * Phase 01: Source -> Bytecode -> JVM
 * Motto: Java source is for humans; bytecode is for the virtual machine.
 */
public class Phase01Demo {
    private final String topic;

    public Phase01Demo() {
        this.topic = "Source -> Bytecode -> JVM";
    }

    public String execute() {
        return "Executed " + topic + ": Java source is for humans; bytecode is for the virtual machine.";
    }

    public static void main(String[] args) {
        Phase01Demo demo = new Phase01Demo();
        System.out.println(demo.execute());
    }
}
