package lld.foundations.money;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 08: Money Value Object Tests")
class MoneyTest {
    @Test
    void shouldAddMatchingCurrencies() {
        Money m1 = Money.of(50.0, "USD");
        Money m2 = Money.of(25.5, "USD");
        Money result = m1.add(m2);

        assertThat(result.amount()).isEqualByComparingTo("75.5");
        assertThat(result.currency().getCurrencyCode()).isEqualTo("USD");
    }

    @Test
    void shouldRejectNegativeMoneyAtConstruction() {
        assertThatThrownBy(() -> Money.of(-10.0, "USD"))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Money amount cannot be negative");
    }

    @Test
    void shouldRejectMismatchedCurrenciesOnAdd() {
        Money usd = Money.of(10.0, "USD");
        Money eur = Money.of(10.0, "EUR");

        assertThatThrownBy(() -> usd.add(eur))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Cannot add different currencies");
    }
}
