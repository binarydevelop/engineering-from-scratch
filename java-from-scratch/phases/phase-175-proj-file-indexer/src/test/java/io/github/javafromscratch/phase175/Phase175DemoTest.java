package io.github.javafromscratch.phase175;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 175: Project 5: High-Performance File Indexer Verification")
class Phase175DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase175Demo demo = new Phase175Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 5: High-Performance File Indexer"), "Output must contain lesson topic");
        assertTrue(result.contains("Traverse directory trees concurrently to build a searchable inverted index."), "Output must contain lesson motto");
    }
}
