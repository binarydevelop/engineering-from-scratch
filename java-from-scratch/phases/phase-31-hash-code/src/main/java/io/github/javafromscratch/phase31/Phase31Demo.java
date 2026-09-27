package io.github.javafromscratch.phase31;

/**
 * Phase 31: The hashCode and equals Contract
 * Motto: Equal objects MUST produce equal hash codes; violate this and hash sets break.
 */
public class Phase31Demo {
    private final String topic;

    public Phase31Demo() {
        this.topic = "The hashCode and equals Contract";
    }

    public String execute() {
        return "Executed " + topic + ": Equal objects MUST produce equal hash codes; violate this and hash sets break.";
    }

    public static void main(String[] args) {
        Phase31Demo demo = new Phase31Demo();
        System.out.println(demo.execute());
    }
}
