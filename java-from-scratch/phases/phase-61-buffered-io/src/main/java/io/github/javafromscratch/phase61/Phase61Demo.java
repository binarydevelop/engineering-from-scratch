package io.github.javafromscratch.phase61;

/**
 * Phase 61: Buffered I/O & Syscall Overhead
 * Motto: Issuing a kernel syscall for every byte is a 1000x performance penalty.
 */
public class Phase61Demo {
    private final String topic;

    public Phase61Demo() {
        this.topic = "Buffered I/O & Syscall Overhead";
    }

    public String execute() {
        return "Executed " + topic + ": Issuing a kernel syscall for every byte is a 1000x performance penalty.";
    }

    public static void main(String[] args) {
        Phase61Demo demo = new Phase61Demo();
        System.out.println(demo.execute());
    }
}
