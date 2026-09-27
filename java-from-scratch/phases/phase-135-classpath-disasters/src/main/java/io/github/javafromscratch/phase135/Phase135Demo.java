package io.github.javafromscratch.phase135;

/**
 * Phase 135: The Classpath: Mechanics & Disasters
 * Motto: The classpath is an ordered list of directories and JARs scanned for .class files.
 */
public class Phase135Demo {
    private final String topic;

    public Phase135Demo() {
        this.topic = "The Classpath: Mechanics & Disasters";
    }

    public String execute() {
        return "Executed " + topic + ": The classpath is an ordered list of directories and JARs scanned for .class files.";
    }

    public static void main(String[] args) {
        Phase135Demo demo = new Phase135Demo();
        System.out.println(demo.execute());
    }
}
