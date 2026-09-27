package lld.refactoringlabs.lab_15_leaky_abstraction_cart.broken;

// ❌ CODE SMELL: Demonstrates anti-pattern before refactoring
public class LegacySystem {
    public String data;
    public double amount;

    public void executeProcess(boolean flag, String type) {
        if (flag) {
            if (type.equals("A")) {
                amount += 10.0;
            } else {
                amount += 20.0;
            }
        }
    }
}
