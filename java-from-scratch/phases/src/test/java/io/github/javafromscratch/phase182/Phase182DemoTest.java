package io.github.javafromscratch.phase182;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 182: Project 12: Mini Object-Relational Mapper Verification")
class Phase182DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase182Demo demo = new Phase182Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 12: Mini Object-Relational Mapper"), "Output must contain lesson topic");
        assertTrue(result.contains("Map SQL rows to Java domain objects via reflection and metadata."), "Output must contain lesson motto");
    }
}
