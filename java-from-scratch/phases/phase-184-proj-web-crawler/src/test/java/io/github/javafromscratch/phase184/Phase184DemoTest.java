package io.github.javafromscratch.phase184;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 184: Project 14: Concurrent Web Crawler Verification")
class Phase184DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase184Demo demo = new Phase184Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Project 14: Concurrent Web Crawler"), "Output must contain lesson topic");
        assertTrue(result.contains("Build an asynchronous web crawler with virtual threads and rate limits."), "Output must contain lesson motto");
    }
}
