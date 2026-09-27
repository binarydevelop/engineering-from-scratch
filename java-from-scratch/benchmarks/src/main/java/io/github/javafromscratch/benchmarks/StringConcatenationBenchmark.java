package io.github.javafromscratch.benchmarks;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Thread)
@Warmup(iterations = 2, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 3, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(1)
public class StringConcatenationBenchmark {

    @Param({"10", "100"})
    public int iterations;

    @Benchmark
    public void testNaiveConcat(Blackhole bh) {
        String s = "";
        for (int i = 0; i < iterations; i++) {
            s += i;
        }
        bh.consume(s);
    }

    @Benchmark
    public void testStringBuilder(Blackhole bh) {
        StringBuilder sb = new StringBuilder(iterations * 4);
        for (int i = 0; i < iterations; i++) {
            sb.append(i);
        }
        bh.consume(sb.toString());
    }
}
