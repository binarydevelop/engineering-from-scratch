package io.github.javafromscratch.phase127;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 127: JPA and Hibernate Basics Verification")
class Phase127DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase127Demo demo = new Phase127Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("JPA and Hibernate Basics"), "Output must contain lesson topic");
        assertTrue(result.contains("An ORM manages entity state transitions and generates SQL on your behalf."), "Output must contain lesson motto");
    }
}
