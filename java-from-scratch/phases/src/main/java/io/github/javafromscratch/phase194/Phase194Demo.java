package io.github.javafromscratch.phase194;

/**
 * Phase 194: Broken Lab 08: Leaked JDBC Connection Pool
 * Motto: Diagnose unclosed database connections exhausting the pool.
 */
public class Phase194Demo {
    private final String topic;

    public Phase194Demo() {
        this.topic = "Broken Lab 08: Leaked JDBC Connection Pool";
    }

    public String execute() {
        return "Executed " + topic + ": Diagnose unclosed database connections exhausting the pool.";
    }

    public static void main(String[] args) {
        Phase194Demo demo = new Phase194Demo();
        System.out.println(demo.execute());
    }
}
