from __future__ import annotations

from dataclasses import dataclass, asdict
from math import ceil
from typing import Dict


@dataclass(frozen=True)
class FunnelInputs:
    monthly_visitors: int = 8000
    event_view_rate: float = 0.42
    checkout_start_rate: float = 0.16
    purchase_completion_rate: float = 0.62
    average_order_value: float = 32.0
    repeat_booking_rate: float = 0.18


@dataclass(frozen=True)
class FunnelUplifts:
    event_view_uplift: float = 0.08
    checkout_start_uplift: float = 0.10
    purchase_completion_uplift: float = 0.12
    repeat_booking_uplift: float = 0.15


def _cap_rate(value: float) -> float:
    return max(0.0, min(1.0, value))


def calculate_funnel(inputs: FunnelInputs) -> Dict[str, float]:
    visitors = float(max(inputs.monthly_visitors, 0))
    event_views = visitors * _cap_rate(inputs.event_view_rate)
    checkout_starts = event_views * _cap_rate(inputs.checkout_start_rate)
    purchases = checkout_starts * _cap_rate(inputs.purchase_completion_rate)
    revenue = purchases * max(inputs.average_order_value, 0.0)
    repeat_bookings = purchases * _cap_rate(inputs.repeat_booking_rate)
    repeat_revenue = repeat_bookings * max(inputs.average_order_value, 0.0)

    return {
        "Visitors": visitors,
        "Event / product views": event_views,
        "Checkout starts": checkout_starts,
        "Purchases": purchases,
        "Revenue": revenue,
        "Repeat bookings": repeat_bookings,
        "Repeat revenue": repeat_revenue,
        "Visitor-to-purchase conversion": (purchases / visitors) if visitors else 0.0,
    }


def apply_uplifts(inputs: FunnelInputs, uplifts: FunnelUplifts) -> FunnelInputs:
    return FunnelInputs(
        monthly_visitors=inputs.monthly_visitors,
        event_view_rate=_cap_rate(inputs.event_view_rate * (1 + uplifts.event_view_uplift)),
        checkout_start_rate=_cap_rate(inputs.checkout_start_rate * (1 + uplifts.checkout_start_uplift)),
        purchase_completion_rate=_cap_rate(
            inputs.purchase_completion_rate * (1 + uplifts.purchase_completion_uplift)
        ),
        average_order_value=inputs.average_order_value,
        repeat_booking_rate=_cap_rate(
            inputs.repeat_booking_rate * (1 + uplifts.repeat_booking_uplift)
        ),
    )


def compare_scenarios(inputs: FunnelInputs, uplifts: FunnelUplifts) -> Dict[str, Dict[str, float]]:
    baseline = calculate_funnel(inputs)
    improved_inputs = apply_uplifts(inputs, uplifts)
    improved = calculate_funnel(improved_inputs)
    delta = {key: improved.get(key, 0.0) - baseline.get(key, 0.0) for key in baseline}
    return {
        "baseline": baseline,
        "improved": improved,
        "delta": delta,
        "improved_inputs": asdict(improved_inputs),
    }


def two_proportion_sample_size(
    baseline_rate: float,
    relative_uplift: float,
    z_alpha: float = 1.96,
    z_power: float = 0.84,
) -> int:
    """Approximate sample size per variant for a two-sided two-proportion test.

    Intended for planning only; it is not a substitute for a production experimentation
    platform or a full statistical power analysis.
    """
    p1 = _cap_rate(baseline_rate)
    p2 = _cap_rate(p1 * (1 + max(relative_uplift, 0.0)))
    if p1 <= 0 or p2 <= p1 or p2 >= 1:
        return 0

    p_bar = (p1 + p2) / 2
    numerator = (
        z_alpha * (2 * p_bar * (1 - p_bar)) ** 0.5
        + z_power * (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5
    ) ** 2
    denominator = (p2 - p1) ** 2
    return ceil(numerator / denominator)
