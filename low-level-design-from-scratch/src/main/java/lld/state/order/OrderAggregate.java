package lld.state.order;

import java.util.Objects;

public class OrderAggregate {
    private final String orderId;
    private OrderStatus status;

    public OrderAggregate(String orderId) {
        if (orderId == null || orderId.isBlank()) {
            throw new IllegalArgumentException("Order ID cannot be blank");
        }
        this.orderId = orderId;
        this.status = OrderStatus.CREATED;
    }

    public synchronized void transitionTo(OrderStatus nextStatus) {
        Objects.requireNonNull(nextStatus, "Next status cannot be null");
        if (!this.status.canTransitionTo(nextStatus)) {
            throw new IllegalStateException("Illegal state transition from " + this.status + " to " + nextStatus);
        }
        this.status = nextStatus;
    }

    public OrderStatus getStatus() {
        return status;
    }

    public String getOrderId() {
        return orderId;
    }
}
