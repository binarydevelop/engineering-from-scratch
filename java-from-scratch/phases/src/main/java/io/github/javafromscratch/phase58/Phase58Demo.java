package io.github.javafromscratch.phase58;

/**
 * Phase 58: Try-With-Resources & AutoCloseable
 * Motto: Manual resource cleanup will eventually leak; automate it with AutoCloseable.
 */
public class Phase58Demo {
    private final String topic;

    public Phase58Demo() {
        this.topic = "Try-With-Resources & AutoCloseable";
    }

    public String execute() {
        return "Executed " + topic + ": Manual resource cleanup will eventually leak; automate it with AutoCloseable.";
    }

    public static void main(String[] args) {
        Phase58Demo demo = new Phase58Demo();
        System.out.println(demo.execute());
    }
}
