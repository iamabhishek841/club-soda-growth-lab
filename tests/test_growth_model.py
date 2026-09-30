from src.growth_model import FunnelInputs, FunnelUplifts, calculate_funnel, compare_scenarios, two_proportion_sample_size


def test_funnel_math():
    f = calculate_funnel(
        FunnelInputs(
            monthly_visitors=1000,
            event_view_rate=0.5,
            checkout_start_rate=0.2,
            purchase_completion_rate=0.5,
            average_order_value=20,
            repeat_booking_rate=0.1,
        )
    )
    assert f["Event / product views"] == 500
    assert f["Checkout starts"] == 100
    assert f["Purchases"] == 50
    assert f["Revenue"] == 1000
    assert f["Repeat bookings"] == 5


def test_improvement_scenario_is_non_decreasing():
    result = compare_scenarios(
        FunnelInputs(),
        FunnelUplifts(0.1, 0.1, 0.1, 0.1),
    )
    assert result["improved"]["Purchases"] >= result["baseline"]["Purchases"]
    assert result["improved"]["Revenue"] >= result["baseline"]["Revenue"]


def test_ab_sample_size_is_positive():
    assert two_proportion_sample_size(0.10, 0.20) > 0
