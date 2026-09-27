package io.github.javafromscratch.phase170;

/**
 * Phase 170: The Native Boundary & JNI/FFM
 * Motto: The JVM interacts with the operating system kernel and hardware via native code.
 */
public class Phase170Demo {
    private final String topic;

    public Phase170Demo() {
        this.topic = "The Native Boundary & JNI/FFM";
    }

    public String execute() {
        return "Executed " + topic + ": The JVM interacts with the operating system kernel and hardware via native code.";
    }

    public static void main(String[] args) {
        Phase170Demo demo = new Phase170Demo();
        System.out.println(demo.execute());
    }
}
