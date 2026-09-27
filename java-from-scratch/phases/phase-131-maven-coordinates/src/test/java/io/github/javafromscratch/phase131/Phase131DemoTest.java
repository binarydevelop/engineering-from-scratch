package io.github.javafromscratch.phase131;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 131: Maven Coordinates & Dependency Tree Verification")
class Phase131DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase131Demo demo = new Phase131Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Maven Coordinates & Dependency Tree"), "Output must contain lesson topic");
        assertTrue(result.contains("GroupId, ArtifactId, and Version uniquely identify libraries in global repositories."), "Output must contain lesson motto");
    }
}
