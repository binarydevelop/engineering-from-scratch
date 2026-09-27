package io.github.javafromscratch.phase110;

/**
 * Phase 110: CompletableFuture Threading Rules
 * Motto: Know which executor runs each stage of your async pipeline.
 */
public class Phase110Demo {
    private final String topic;

    public Phase110Demo() {
        this.topic = "CompletableFuture Threading Rules";
    }

    public String execute() {
        return "Executed " + topic + ": Know which executor runs each stage of your async pipeline.";
    }

    public static void main(String[] args) {
        Phase110Demo demo = new Phase110Demo();
        System.out.println(demo.execute());
    }
}
