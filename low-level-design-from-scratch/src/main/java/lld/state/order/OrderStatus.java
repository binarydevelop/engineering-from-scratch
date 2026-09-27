package lld.state.order;

public enum OrderStatus {
    CREATED {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return next == PAID || next == CANCELLED;
        }
    },
    PAID {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return next == SHIPPED || next == CANCELLED;
        }
    },
    SHIPPED {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return next == DELIVERED;
        }
    },
    DELIVERED {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return false;
        }
    },
    CANCELLED {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return false;
        }
    };

    public abstract boolean canTransitionTo(OrderStatus next);
}
