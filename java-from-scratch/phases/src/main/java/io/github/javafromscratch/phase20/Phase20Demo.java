package io.github.javafromscratch.phase20;

/**
 * Phase 20: Packages and Namespaces
 * Motto: Packages partition the global type space and enforce directory structures.
 */
public class Phase20Demo {
    private final String topic;

    public Phase20Demo() {
        this.topic = "Packages and Namespaces";
    }

    public String execute() {
        return "Executed " + topic + ": Packages partition the global type space and enforce directory structures.";
    }

    public static void main(String[] args) {
        Phase20Demo demo = new Phase20Demo();
        System.out.println(demo.execute());
    }
}
