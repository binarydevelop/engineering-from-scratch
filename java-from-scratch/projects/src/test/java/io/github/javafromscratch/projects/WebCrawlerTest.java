package io.github.javafromscratch.projects;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Concurrent Asynchronous Web Crawler Test Suite")
class WebCrawlerTest {

    @Test
    @DisplayName("Should initialize and execute operations reliably")
    void shouldExecuteOperations() {
        WebCrawler instance = new WebCrawler("Concurrent Asynchronous Web Crawler");
        assertEquals("Concurrent Asynchronous Web Crawler", instance.getName());
        assertEquals(1, instance.performOperation());
        assertEquals(2, instance.performOperation());
        assertEquals(2, instance.getOperationCount());
    }
}
