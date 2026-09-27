package io.github.javafromscratch.phase177;

/**
 * Phase 177: Project 7: JDBC CRUD Service
 * Motto: Build a transactional database-backed service with connection pooling.
 */
public class Phase177Demo {
    private final String topic;

    public Phase177Demo() {
        this.topic = "Project 7: JDBC CRUD Service";
    }

    public String execute() {
        return "Executed " + topic + ": Build a transactional database-backed service with connection pooling.";
    }

    public static void main(String[] args) {
        Phase177Demo demo = new Phase177Demo();
        System.out.println(demo.execute());
    }
}
