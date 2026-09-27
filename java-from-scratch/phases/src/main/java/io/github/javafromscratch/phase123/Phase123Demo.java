package io.github.javafromscratch.phase123;

/**
 * Phase 123: SQL Injection & PreparedStatement
 * Motto: Never concatenate user input into SQL; parameterize with PreparedStatement.
 */
public class Phase123Demo {
    private final String topic;

    public Phase123Demo() {
        this.topic = "SQL Injection & PreparedStatement";
    }

    public String execute() {
        return "Executed " + topic + ": Never concatenate user input into SQL; parameterize with PreparedStatement.";
    }

    public static void main(String[] args) {
        Phase123Demo demo = new Phase123Demo();
        System.out.println(demo.execute());
    }
}
