package lld.capstones.locker;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

public class PackageLockerSystem {
    public enum CompartmentSize { SMALL, MEDIUM, LARGE }

    public static class Compartment {
        private final String compartmentId;
        private final CompartmentSize size;
        private boolean occupied;
        private String assignedPin;

        public Compartment(String compartmentId, CompartmentSize size) {
            this.compartmentId = compartmentId;
            this.size = size;
            this.occupied = false;
        }

        public boolean depositPackage(String pin) {
            if (occupied) return false;
            this.occupied = true;
            this.assignedPin = pin;
            return true;
        }

        public boolean pickupPackage(String pin) {
            if (!occupied || assignedPin == null || !assignedPin.equals(pin)) {
                return false;
            }
            this.occupied = false;
            this.assignedPin = null;
            return true;
        }

        public String getCompartmentId() { return compartmentId; }
        public CompartmentSize getSize() { return size; }
        public boolean isOccupied() { return occupied; }
    }

    private final List<Compartment> compartments = new ArrayList<>();

    public void addCompartment(Compartment compartment) {
        compartments.add(compartment);
    }

    public synchronized Optional<Compartment> deposit(CompartmentSize size, String pin) {
        for (Compartment c : compartments) {
            if (!c.isOccupied() && c.getSize() == size) {
                if (c.depositPackage(pin)) {
                    return Optional.of(c);
                }
            }
        }
        return Optional.empty();
    }

    public synchronized boolean pickup(String compartmentId, String pin) {
        for (Compartment c : compartments) {
            if (c.getCompartmentId().equals(compartmentId)) {
                return c.pickupPackage(pin);
            }
        }
        return false;
    }

    public List<Compartment> getCompartments() {
        return Collections.unmodifiableList(compartments);
    }
}
