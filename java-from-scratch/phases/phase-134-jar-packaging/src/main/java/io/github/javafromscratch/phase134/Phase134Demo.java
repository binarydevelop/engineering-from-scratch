package io.github.javafromscratch.phase134;

/**
 * Phase 134: Anatomy of a JAR File
 * Motto: A JAR is a ZIP archive with a META-INF/MANIFEST.MF contract.
 */
public class Phase134Demo {
    private final String topic;

    public Phase134Demo() {
        this.topic = "Anatomy of a JAR File";
    }

    public String execute() {
        return "Executed " + topic + ": A JAR is a ZIP archive with a META-INF/MANIFEST.MF contract.";
    }

    public static void main(String[] args) {
        Phase134Demo demo = new Phase134Demo();
        System.out.println(demo.execute());
    }
}
