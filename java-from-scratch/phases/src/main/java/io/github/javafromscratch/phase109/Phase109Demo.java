package io.github.javafromscratch.phase109;

/**
 * Phase 109: Pipelines: CompletableFuture
 * Motto: Build non-blocking reactive pipelines via functional composition.
 */
public class Phase109Demo {
    private final String topic;

    public Phase109Demo() {
        this.topic = "Pipelines: CompletableFuture";
    }

    public String execute() {
        return "Executed " + topic + ": Build non-blocking reactive pipelines via functional composition.";
    }

    public static void main(String[] args) {
        Phase109Demo demo = new Phase109Demo();
        System.out.println(demo.execute());
    }
}
