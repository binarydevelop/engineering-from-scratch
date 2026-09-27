package lld.capstones.locker;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 146: Package Locker System Mental Model Tests")
class PackageLockerSystemTest {
    @Test
    void shouldDepositAndPickupPackageWithPin() {
        PackageLockerSystem locker = new PackageLockerSystem();
        locker.addCompartment(new PackageLockerSystem.Compartment("C-1", PackageLockerSystem.CompartmentSize.MEDIUM));

        var assigned = locker.deposit(PackageLockerSystem.CompartmentSize.MEDIUM, "PIN-1234");
        assertThat(assigned).isPresent();
        assertThat(assigned.get().isOccupied()).isTrue();

        // Pickup with wrong pin fails
        boolean wrongPin = locker.pickup("C-1", "WRONG-PIN");
        assertThat(wrongPin).isFalse();
        assertThat(assigned.get().isOccupied()).isTrue();

        // Pickup with valid pin succeeds and frees locker
        boolean validPickup = locker.pickup("C-1", "PIN-1234");
        assertThat(validPickup).isTrue();
        assertThat(assigned.get().isOccupied()).isFalse();
    }
}
