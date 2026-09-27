package lld.state.order;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 33: Order State Transition Invariant Tests")
class OrderAggregateTest {
    @Test
    void shouldFollowValidLifecycleTransitions() {
        OrderAggregate order = new OrderAggregate("ORD-99");
        assertThat(order.getStatus()).isEqualTo(OrderStatus.CREATED);

        order.transitionTo(OrderStatus.PAID);
        order.transitionTo(OrderStatus.SHIPPED);
        order.transitionTo(OrderStatus.DELIVERED);

        assertThat(order.getStatus()).isEqualTo(OrderStatus.DELIVERED);
    }

    @Test
    void shouldRejectIllegalTransitionFromDeliveredToCancelled() {
        OrderAggregate order = new OrderAggregate("ORD-99");
        order.transitionTo(OrderStatus.PAID);
        order.transitionTo(OrderStatus.SHIPPED);
        order.transitionTo(OrderStatus.DELIVERED);

        assertThatThrownBy(() -> order.transitionTo(OrderStatus.CANCELLED))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("Illegal state transition from DELIVERED to CANCELLED");
    }
}
