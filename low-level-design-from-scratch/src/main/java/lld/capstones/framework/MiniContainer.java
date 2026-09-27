package lld.capstones.framework;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class MiniContainer {
    private final Map<Class<?>, Object> singletons = new HashMap<>();

    public <T> void registerSingleton(Class<T> type, T instance) {
        Objects.requireNonNull(type, "Type cannot be null");
        Objects.requireNonNull(instance, "Instance cannot be null");
        singletons.put(type, instance);
    }

    @SuppressWarnings("unchecked")
    public <T> T resolve(Class<T> type) {
        Object instance = singletons.get(type);
        if (instance == null) {
            throw new IllegalArgumentException("No registered binding for type: " + type.getName());
        }
        return (T) instance;
    }
}
