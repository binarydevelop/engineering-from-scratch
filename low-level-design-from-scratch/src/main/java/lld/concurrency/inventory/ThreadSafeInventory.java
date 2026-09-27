package lld.concurrency.inventory;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadSafeInventory {
    private final ConcurrentHashMap<String, AtomicInteger> stock = new ConcurrentHashMap<>();

    public void addStock(String sku, int quantity) {
        if (quantity <= 0) throw new IllegalArgumentException("Quantity must be positive");
        stock.computeIfAbsent(sku, k -> new AtomicInteger(0)).addAndGet(quantity);
    }

    public boolean reserveStock(String sku, int quantity) {
        if (quantity <= 0) throw new IllegalArgumentException("Quantity must be positive");
        AtomicInteger current = stock.get(sku);
        if (current == null) return false;

        while (true) {
            int available = current.get();
            if (available < quantity) {
                return false;
            }
            if (current.compareAndSet(available, available - quantity)) {
                return true;
            }
        }
    }

    public int getAvailableStock(String sku) {
        AtomicInteger current = stock.get(sku);
        return current != null ? current.get() : 0;
    }
}
