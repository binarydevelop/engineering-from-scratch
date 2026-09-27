package lld.refactoringlabs.lab_21_interface_pollution_worker.broken;

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
