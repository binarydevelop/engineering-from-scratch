# JMH Microbenchmarking Suite

Rigorous microbenchmarks configured with JMH to measure real JVM performance while defeating dead-code elimination, constant folding, and warmup artifacts.

## Benchmarks Included:
1. `StringConcatenationBenchmark`: Naive `+` operator vs pre-sized `StringBuilder`.
2. `ListIterationBenchmark`: Sequential memory array access vs pointer chasing node chain.
3. `BoxingBenchmark`: Primitive `int` loop vs `java.lang.Integer` heap allocation loop.
4. `LockContentionBenchmark`: `synchronized` monitor vs `ReentrantLock` vs lock-free `AtomicInteger`.
5. `VirtualThreadBenchmark`: Platform thread creation vs Virtual Thread creation under blocking delay.

## Running Benchmarks
```bash
mvn clean package -pl benchmarks
java -jar benchmarks/target/benchmarks.jar -f 1 -wi 3 -i 5
```
