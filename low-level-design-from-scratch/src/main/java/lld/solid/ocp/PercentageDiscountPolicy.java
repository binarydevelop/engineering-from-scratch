package lld.solid.ocp;

public class PercentageDiscountPolicy implements DiscountPolicy {
    private final double percentage;

    public PercentageDiscountPolicy(double percentage) {
        if (percentage < 0.0 || percentage > 100.0) {
            throw new IllegalArgumentException("Percentage must be between 0 and 100");
        }
        this.percentage = percentage;
    }

    @Override
    public double applyDiscount(double originalAmount) {
        return originalAmount * (1.0 - (percentage / 100.0));
    }
}
