package lld.problems.parkinglot;

import java.time.Duration;
import java.time.Instant;
import java.util.*;

public class ParkingLot {

    public enum VehicleType { MOTORCYCLE, CAR, TRUCK }
    public enum SpotType { MOTORCYCLE, COMPACT, LARGE }

    public record Vehicle(String licensePlate, VehicleType type) {
        public Vehicle {
            Objects.requireNonNull(licensePlate, "License plate cannot be null");
            Objects.requireNonNull(type, "Vehicle type cannot be null");
        }
    }

    public static class ParkingSpot {
        private final String spotId;
        private final SpotType spotType;
        private boolean occupied;
        private Vehicle currentVehicle;

        public ParkingSpot(String spotId, SpotType spotType) {
            this.spotId = spotId;
            this.spotType = spotType;
            this.occupied = false;
        }

        public boolean canFit(Vehicle vehicle) {
            return switch (vehicle.type()) {
                case MOTORCYCLE -> true;
                case CAR -> spotType == SpotType.COMPACT || spotType == SpotType.LARGE;
                case TRUCK -> spotType == SpotType.LARGE;
            };
        }

        public synchronized void occupy(Vehicle vehicle) {
            if (occupied) throw new IllegalStateException("Spot already occupied");
            if (!canFit(vehicle)) throw new IllegalArgumentException("Vehicle does not fit in this spot");
            this.occupied = true;
            this.currentVehicle = vehicle;
        }

        public synchronized void release() {
            if (!occupied) throw new IllegalStateException("Spot is already vacant");
            this.occupied = false;
            this.currentVehicle = null;
        }

        public String getSpotId() { return spotId; }
        public SpotType getSpotType() { return spotType; }
        public boolean isOccupied() { return occupied; }
        public Vehicle getCurrentVehicle() { return currentVehicle; }
    }

    public record Ticket(String ticketId, Vehicle vehicle, String spotId, Instant entryTime) {
        public Ticket {
            Objects.requireNonNull(ticketId);
            Objects.requireNonNull(vehicle);
            Objects.requireNonNull(spotId);
            Objects.requireNonNull(entryTime);
        }
    }

    public interface PricingStrategy {
        long calculateFeeInCents(Ticket ticket, Instant exitTime);
    }

    public static class StandardHourlyPricing implements PricingStrategy {
        private final long hourlyRateInCents;

        public StandardHourlyPricing(long hourlyRateInCents) {
            this.hourlyRateInCents = hourlyRateInCents;
        }

        @Override
        public long calculateFeeInCents(Ticket ticket, Instant exitTime) {
            long hours = Math.max(1, Duration.between(ticket.entryTime(), exitTime).toHours());
            long multiplier = switch (ticket.vehicle().type()) {
                case MOTORCYCLE -> 1;
                case CAR -> 2;
                case TRUCK -> 3;
            };
            return hours * hourlyRateInCents * multiplier;
        }
    }

    private final String lotId;
    private final List<ParkingSpot> spots = new ArrayList<>();
    private final Map<String, Ticket> activeTickets = new HashMap<>();
    private PricingStrategy pricingStrategy;

    public ParkingLot(String lotId, PricingStrategy pricingStrategy) {
        this.lotId = Objects.requireNonNull(lotId);
        this.pricingStrategy = Objects.requireNonNull(pricingStrategy);
    }

    public synchronized void addSpot(ParkingSpot spot) {
        spots.add(spot);
    }

    public synchronized Ticket parkVehicle(Vehicle vehicle, Instant entryTime) {
        ParkingSpot availableSpot = spots.stream()
                .filter(s -> !s.isOccupied() && s.canFit(vehicle))
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("No available spot for vehicle: " + vehicle.type()));

        availableSpot.occupy(vehicle);
        String ticketId = "TICK-" + UUID.randomUUID().toString().substring(0, 8);
        Ticket ticket = new Ticket(ticketId, vehicle, availableSpot.getSpotId(), entryTime);
        activeTickets.put(ticketId, ticket);
        return ticket;
    }

    public synchronized long exitVehicle(String ticketId, Instant exitTime) {
        Ticket ticket = activeTickets.remove(ticketId);
        if (ticket == null) {
            throw new IllegalArgumentException("Invalid ticket ID: " + ticketId);
        }
        ParkingSpot spot = spots.stream()
                .filter(s -> s.getSpotId().equals(ticket.spotId()))
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("Spot not found"));

        spot.release();
        return pricingStrategy.calculateFeeInCents(ticket, exitTime);
    }

    public synchronized void setPricingStrategy(PricingStrategy strategy) {
        this.pricingStrategy = Objects.requireNonNull(strategy);
    }

    public synchronized long getAvailableSpotCount() {
        return spots.stream().filter(s -> !s.isOccupied()).count();
    }
}
