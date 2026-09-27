package lld.solid.ocp;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 21: OCP Discount Strategy Tests")
class DiscountPolicyTest {
    @Test
    void shouldApplyFlatDiscountWithoutModifyingCoreLogic() {
        DiscountPolicy flat = new FlatDiscountPolicy(20.0);
        assertThat(flat.applyDiscount(100.0)).isEqualTo(80.0);
    }

    @Test
    void shouldApplyPercentageDiscountPolymorphically() {
        DiscountPolicy percent = new PercentageDiscountPolicy(15.0);
        assertThat(percent.applyDiscount(200.0)).isEqualTo(170.0);
    }
}
