package lld.capstones.framework;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 144: Mini Framework IoC Container Tests")
class MiniContainerTest {
    interface Notifier { String send(String msg); }
    static class SmtpNotifier implements Notifier {
        @Override public String send(String msg) { return "SENT: " + msg; }
    }

    @Test
    void shouldRegisterAndResolveBindings() {
        MiniContainer container = new MiniContainer();
        container.registerSingleton(Notifier.class, new SmtpNotifier());

        Notifier notifier = container.resolve(Notifier.class);
        assertThat(notifier.send("Hello LLD")).isEqualTo("SENT: Hello LLD");
    }

    @Test
    void shouldThrowWhenResolvingUnregisteredType() {
        MiniContainer container = new MiniContainer();
        assertThatThrownBy(() -> container.resolve(String.class))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("No registered binding");
    }
}
