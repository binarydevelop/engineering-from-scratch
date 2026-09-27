package io.github.javafromscratch.phase139;

/**
 * Phase 139: Test Doubles: Fakes, Stubs, Mocks
 * Motto: Fakes have working implementations; stubs return canned data; mocks verify interactions.
 */
public class Phase139Demo {
    private final String topic;

    public Phase139Demo() {
        this.topic = "Test Doubles: Fakes, Stubs, Mocks";
    }

    public String execute() {
        return "Executed " + topic + ": Fakes have working implementations; stubs return canned data; mocks verify interactions.";
    }

    public static void main(String[] args) {
        Phase139Demo demo = new Phase139Demo();
        System.out.println(demo.execute());
    }
}
