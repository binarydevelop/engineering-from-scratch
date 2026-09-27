package io.github.javafromscratch.phase39;

/**
 * Phase 39: HashMap from First Principles
 * Motto: Hash functions project infinite key spaces into finite bucket arrays.
 */
public class Phase39Demo {
    private final String topic;

    public Phase39Demo() {
        this.topic = "HashMap from First Principles";
    }

    public String execute() {
        return "Executed " + topic + ": Hash functions project infinite key spaces into finite bucket arrays.";
    }

    public static void main(String[] args) {
        Phase39Demo demo = new Phase39Demo();
        System.out.println(demo.execute());
    }
}
