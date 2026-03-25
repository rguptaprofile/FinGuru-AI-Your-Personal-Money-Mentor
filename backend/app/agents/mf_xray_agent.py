from app.models.schemas import MFPortfolioInput, MFPortfolioResponse


def analyze_mf_portfolio(payload: MFPortfolioInput) -> MFPortfolioResponse:
    xirr = ((payload.current_value / payload.invested_amount) ** (1 / payload.years_held) - 1) * 100
    benchmark_delta = xirr - payload.benchmark_return_percent
    expense_drag = payload.current_value * (payload.expense_ratio_percent / 100)

    if payload.expense_ratio_percent >= 2:
        overlap_risk = "high"
    elif payload.expense_ratio_percent >= 1.2:
        overlap_risk = "medium"
    else:
        overlap_risk = "low"

    rebalance = [
        "Reduce high expense-ratio funds and prioritize low-cost index core.",
        "Check category overlap and cap duplicate large-cap exposure.",
        "Review underperforming funds vs benchmark for 3-year consistency.",
    ]

    return MFPortfolioResponse(
        estimated_xirr_percent=round(xirr, 2),
        benchmark_comparison_percent=round(benchmark_delta, 2),
        expense_drag_amount=round(expense_drag, 2),
        overlap_risk_level=overlap_risk,
        rebalance_plan=rebalance,
    )
