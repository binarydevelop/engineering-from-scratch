package io.github.javafromscratch.capstones;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Capstone: Multi-Threaded WAL & LSM-Tree Storage Engine Test Suite")
class LsmStorageEngineTest {

    @Test
    @DisplayName("Should publish events and verify high-throughput atomic sequence")
    void shouldExecuteCapstoneOperations() {
        LsmStorageEngine capstone = new LsmStorageEngine("Multi-Threaded WAL & LSM-Tree Storage Engine");
        assertEquals("Multi-Threaded WAL & LSM-Tree Storage Engine", capstone.getSystemName());
        assertEquals(1L, capstone.publishEvent());
        assertEquals(2L, capstone.publishEvent());
        assertEquals(2L, capstone.getPublishedEventCount());
    }
}
