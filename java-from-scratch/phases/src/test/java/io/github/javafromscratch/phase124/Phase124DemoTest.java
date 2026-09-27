package io.github.javafromscratch.phase124;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 124: Database Transactions: ACID in Java Verification")
class Phase124DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase124Demo demo = new Phase124Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Database Transactions: ACID in Java"), "Output must contain lesson topic");
        assertTrue(result.contains("Transactions group operations into indivisible units of atomic durability."), "Output must contain lesson motto");
    }
}
