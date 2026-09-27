package io.github.javafromscratch.phase128;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 128: The N+1 Query Problem Verification")
class Phase128DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase128Demo demo = new Phase128Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The N+1 Query Problem"), "Output must contain lesson topic");
        assertTrue(result.contains("Naively traversing lazy relations executes N+1 database queries; fix with JOIN FETCH."), "Output must contain lesson motto");
    }
}
