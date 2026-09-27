package io.github.javafromscratch.phase144;

/**
 * Phase 144: SLF4J Facade Architecture
 * Motto: Code against the SLF4J logging facade; bind the logging backend at runtime.
 */
public class Phase144Demo {
    private final String topic;

    public Phase144Demo() {
        this.topic = "SLF4J Facade Architecture";
    }

    public String execute() {
        return "Executed " + topic + ": Code against the SLF4J logging facade; bind the logging backend at runtime.";
    }

    public static void main(String[] args) {
        Phase144Demo demo = new Phase144Demo();
        System.out.println(demo.execute());
    }
}
