package io.github.javafromscratch.phase60;

/**
 * Phase 60: Bytes vs Characters & Encodings
 * Motto: There is no such thing as plain text; there are only bytes and character encodings.
 */
public class Phase60Demo {
    private final String topic;

    public Phase60Demo() {
        this.topic = "Bytes vs Characters & Encodings";
    }

    public String execute() {
        return "Executed " + topic + ": There is no such thing as plain text; there are only bytes and character encodings.";
    }

    public static void main(String[] args) {
        Phase60Demo demo = new Phase60Demo();
        System.out.println(demo.execute());
    }
}
