package lld.lab;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 00: HelloDomain Test Suite")
class HelloDomainTest {

    @Test
    @DisplayName("Should successfully construct HelloDomain with valid name")
    void shouldConstructWithValidName() {
        HelloDomain domain = new HelloDomain("ParkingLotDomain");

        assertThat(domain.getDomainName()).isEqualTo("ParkingLotDomain");
        assertThat(domain.getOperationCount()).isZero();
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"   ", "\t", "\n"})
    @DisplayName("Should reject null or blank domain names to guard invariant")
    void shouldRejectInvalidDomainNames(String invalidName) {
        assertThatThrownBy(() -> new HelloDomain(invalidName))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Domain name cannot be null or blank");
    }

    @Test
    @DisplayName("Should track operation execution and increment operation count")
    void shouldTrackOperations() {
        HelloDomain domain = new HelloDomain("OrderManagement");

        String result1 = domain.executeOperation("CREATE_ORDER");
        String result2 = domain.executeOperation("CONFIRM_PAYMENT");

        assertThat(domain.getOperationCount()).isEqualTo(2);
        assertThat(result1).contains("[OrderManagement]").contains("CREATE_ORDER").contains("total ops: 1");
        assertThat(result2).contains("[OrderManagement]").contains("CONFIRM_PAYMENT").contains("total ops: 2");
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"   "})
    @DisplayName("Should reject blank command operations")
    void shouldRejectBlankCommands(String invalidCommand) {
        HelloDomain domain = new HelloDomain("CoreDomain");

        assertThatThrownBy(() -> domain.executeOperation(invalidCommand))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Command cannot be null or blank");
    }

    @Test
    @DisplayName("Should verify value equality based on domain name")
    void shouldVerifyEquality() {
        HelloDomain domain1 = new HelloDomain("Billing");
        HelloDomain domain2 = new HelloDomain("Billing");
        HelloDomain domain3 = new HelloDomain("Shipping");

        assertThat(domain1).isEqualTo(domain2);
        assertThat(domain1).hasSameHashCodeAs(domain2);
        assertThat(domain1).isNotEqualTo(domain3);
    }
}
