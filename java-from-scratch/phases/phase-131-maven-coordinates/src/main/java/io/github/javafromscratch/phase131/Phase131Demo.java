package io.github.javafromscratch.phase131;

/**
 * Phase 131: Maven Coordinates & Dependency Tree
 * Motto: GroupId, ArtifactId, and Version uniquely identify libraries in global repositories.
 */
public class Phase131Demo {
    private final String topic;

    public Phase131Demo() {
        this.topic = "Maven Coordinates & Dependency Tree";
    }

    public String execute() {
        return "Executed " + topic + ": GroupId, ArtifactId, and Version uniquely identify libraries in global repositories.";
    }

    public static void main(String[] args) {
        Phase131Demo demo = new Phase131Demo();
        System.out.println(demo.execute());
    }
}
