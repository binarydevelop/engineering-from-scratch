package io.github.javafromscratch.phase112;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 112: Resource Throttling: Semaphore Verification")
class Phase112DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase112Demo demo = new Phase112Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("Resource Throttling: Semaphore"), "Output must contain lesson topic");
        assertTrue(result.contains("A semaphore bounds concurrent access to physical resources."), "Output must contain lesson motto");
    }
}
