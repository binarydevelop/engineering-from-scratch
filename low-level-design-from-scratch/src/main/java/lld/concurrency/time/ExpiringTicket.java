package lld.concurrency.time;

import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.Objects;

public class ExpiringTicket {
    private final String ticketId;
    private final Instant createdAt;
    private final Duration validityWindow;
    private final Clock clock;

    public ExpiringTicket(String ticketId, Duration validityWindow, Clock clock) {
        this.ticketId = Objects.requireNonNull(ticketId);
        this.validityWindow = Objects.requireNonNull(validityWindow);
        this.clock = Objects.requireNonNull(clock);
        this.createdAt = clock.instant();
    }

    public boolean isExpired() {
        return clock.instant().isAfter(createdAt.plus(validityWindow));
    }

    public String getTicketId() {
        return ticketId;
    }
}
