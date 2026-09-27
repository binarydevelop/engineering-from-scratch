package io.github.javafromscratch.phase186;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 186: Project 16: In-Memory Relational Database Verification")
class Phase186DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase186Demo demo = new Phase186Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 16: In-Memory Relational Database"), "Output must contain lesson topic");
        assertTrue(result.contains("Build a relational storage engine with indexing and transaction rollback."), "Output must contain lesson motto");
    }
}
