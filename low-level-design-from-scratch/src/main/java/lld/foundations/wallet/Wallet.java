package lld.foundations.wallet;

import java.util.Objects;

public class Wallet {
    private final String walletId;
    private long balanceInCents;

    public Wallet(String walletId, long initialBalanceInCents) {
        if (walletId == null || walletId.isBlank()) {
            throw new IllegalArgumentException("Wallet ID must not be blank");
        }
        if (initialBalanceInCents < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative");
        }
        this.walletId = walletId;
        this.balanceInCents = initialBalanceInCents;
    }

    public synchronized void withdraw(long amountInCents) {
        if (amountInCents <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive");
        }
        if (amountInCents > this.balanceInCents) {
            throw new IllegalStateException("Insufficient wallet balance");
        }
        this.balanceInCents -= amountInCents;
    }

    public synchronized void deposit(long amountInCents) {
        if (amountInCents <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive");
        }
        this.balanceInCents += amountInCents;
    }

    public synchronized long getBalanceInCents() {
        return balanceInCents;
    }

    public String getWalletId() {
        return walletId;
    }
}
