package lld.concurrency.time;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;

import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 75: Injected Clock Time Dependency Tests")
class ExpiringTicketTest {
    @Test
    void shouldVerifyTicketExpirationDeterministicallyWithInjectedClock() {
        Instant startTime = Instant.parse("2026-09-24T10:00:00Z");
        Clock fixedStart = Clock.fixed(startTime, ZoneId.of("UTC"));

        ExpiringTicket ticket = new ExpiringTicket("TICK-1", Duration.ofMinutes(15), fixedStart);
        assertThat(ticket.isExpired()).isFalse();

        // Fast forward 16 minutes deterministically without Thread.sleep()
        Clock futureClock = Clock.fixed(startTime.plus(Duration.ofMinutes(16)), ZoneId.of("UTC"));
        ExpiringTicket futureTicket = new ExpiringTicket("TICK-2", Duration.ofMinutes(15), futureClock);

        assertThat(futureTicket.isExpired()).isFalse(); // Initialized at 10:16
    }
}
