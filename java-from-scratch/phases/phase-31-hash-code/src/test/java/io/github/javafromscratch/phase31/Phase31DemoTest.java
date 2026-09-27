package io.github.javafromscratch.phase31;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 31: The hashCode and equals Contract Verification")
class Phase31DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase31Demo demo = new Phase31Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("The hashCode and equals Contract"), "Output must contain lesson topic");
        assertTrue(result.contains("Equal objects MUST produce equal hash codes; violate this and hash sets break."), "Output must contain lesson motto");
    }
}
