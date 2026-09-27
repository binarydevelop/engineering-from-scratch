package lld.problems.parkinglot;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.time.Instant;
import java.time.temporal.ChronoUnit;

import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 94: Parking Lot System Tests")
class ParkingLotTest {

    @Test
    @DisplayName("Should successfully park compatible vehicle, issue ticket, and release upon exit with fee")
    void shouldParkAndExitVehicle() {
        ParkingLot lot = new ParkingLot("LOT-1", new ParkingLot.StandardHourlyPricing(500)); // $5.00/hr
        lot.addSpot(new ParkingLot.ParkingSpot("S-1", ParkingLot.SpotType.COMPACT));

        ParkingLot.Vehicle car = new ParkingLot.Vehicle("ABC-123", ParkingLot.VehicleType.CAR);
        Instant entry = Instant.now();
        Instant exit = entry.plus(2, ChronoUnit.HOURS);

        ParkingLot.Ticket ticket = lot.parkVehicle(car, entry);
        assertThat(ticket.spotId()).isEqualTo("S-1");
        assertThat(lot.getAvailableSpotCount()).isZero();

        long feeInCents = lot.exitVehicle(ticket.ticketId(), exit);
        // 2 hours * $5.00 * 2 (car multiplier) = $20.00 = 2000 cents
        assertThat(feeInCents).isEqualTo(2000);
        assertThat(lot.getAvailableSpotCount()).isEqualTo(1);
    }

    @Test
    @DisplayName("Should reject truck if only compact spot is available")
    void shouldRejectVehicleWhenNoFittingSpot() {
        ParkingLot lot = new ParkingLot("LOT-1", new ParkingLot.StandardHourlyPricing(500));
        lot.addSpot(new ParkingLot.ParkingSpot("S-1", ParkingLot.SpotType.COMPACT));

        ParkingLot.Vehicle truck = new ParkingLot.Vehicle("TRUCK-99", ParkingLot.VehicleType.TRUCK);

        assertThatThrownBy(() -> lot.parkVehicle(truck, Instant.now()))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("No available spot for vehicle: TRUCK");
    }

    @Test
    @DisplayName("Should throw when exiting with invalid or already used ticket")
    void shouldThrowOnInvalidTicketExit() {
        ParkingLot lot = new ParkingLot("LOT-1", new ParkingLot.StandardHourlyPricing(500));
        lot.addSpot(new ParkingLot.ParkingSpot("S-1", ParkingLot.SpotType.LARGE));

        assertThatThrownBy(() -> lot.exitVehicle("FAKE-TICKET", Instant.now()))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Invalid ticket ID: FAKE-TICKET");
    }
}
