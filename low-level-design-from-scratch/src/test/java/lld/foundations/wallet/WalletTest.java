package lld.foundations.wallet;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 17: Tell Don't Ask Wallet Tests")
class WalletTest {
    @Test
    void shouldExecuteDepositAndWithdrawalBehavior() {
        Wallet wallet = new Wallet("W-100", 5000);
        wallet.deposit(2000);
        wallet.withdraw(4000);

        assertThat(wallet.getBalanceInCents()).isEqualTo(3000);
    }

    @Test
    void shouldRejectOverdraftAtomically() {
        Wallet wallet = new Wallet("W-100", 1000);

        assertThatThrownBy(() -> wallet.withdraw(1500))
                .isInstanceOf(IllegalStateException.class)
                .hasMessage("Insufficient wallet balance");
    }
}
