package io.github.javafromscratch.phase184;

/**
 * Phase 184: Project 14: Concurrent Web Crawler
 * Motto: Build an asynchronous web crawler with virtual threads and rate limits.
 */
public class Phase184Demo {
    private final String topic;

    public Phase184Demo() {
        this.topic = "Project 14: Concurrent Web Crawler";
    }

    public String execute() {
        return "Executed " + topic + ": Build an asynchronous web crawler with virtual threads and rate limits.";
    }

    public static void main(String[] args) {
        Phase184Demo demo = new Phase184Demo();
        System.out.println(demo.execute());
    }
}
