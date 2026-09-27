package io.github.javafromscratch.phase177;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 177: Project 7: JDBC CRUD Service Verification")
class Phase177DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase177Demo demo = new Phase177Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 7: JDBC CRUD Service"), "Output must contain lesson topic");
        assertTrue(result.contains("Build a transactional database-backed service with connection pooling."), "Output must contain lesson motto");
    }
}
