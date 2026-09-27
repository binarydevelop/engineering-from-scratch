package lld.refactoringlabs.lab_22_swallowed_exceptions_payment.broken;

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
