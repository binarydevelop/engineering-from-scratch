package lld.solid.ocp;

public class FlatDiscountPolicy implements DiscountPolicy {
    private final double discountAmount;

    public FlatDiscountPolicy(double discountAmount) {
        if (discountAmount < 0) throw new IllegalArgumentException("Discount cannot be negative");
        this.discountAmount = discountAmount;
    }

    @Override
    public double applyDiscount(double originalAmount) {
        return Math.max(0.0, originalAmount - discountAmount);
    }
}
