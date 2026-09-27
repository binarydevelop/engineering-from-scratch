package io.github.javafromscratch.phase124;

/**
 * Phase 124: Database Transactions: ACID in Java
 * Motto: Transactions group operations into indivisible units of atomic durability.
 */
public class Phase124Demo {
    private final String topic;

    public Phase124Demo() {
        this.topic = "Database Transactions: ACID in Java";
    }

    public String execute() {
        return "Executed " + topic + ": Transactions group operations into indivisible units of atomic durability.";
    }

    public static void main(String[] args) {
        Phase124Demo demo = new Phase124Demo();
        System.out.println(demo.execute());
    }
}
