package io.github.javafromscratch.phase123;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Phase 123: SQL Injection & PreparedStatement Verification")
class Phase123DemoTest {

    @Test
    @DisplayName("Should execute phase logic and verify motto output")
    void shouldExecuteSuccessfully() {
        Phase123Demo demo = new Phase123Demo();
        String result = demo.execute();
        assertNotNull(result, "Result must not be null");
        assertTrue(result.contains("SQL Injection & PreparedStatement"), "Output must contain lesson topic");
        assertTrue(result.contains("Never concatenate user input into SQL; parameterize with PreparedStatement."), "Output must contain lesson motto");
    }
}
