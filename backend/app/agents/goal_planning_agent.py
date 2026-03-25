from __future__ import annotations

from app.models.schemas import AssetAllocation, PlannerResponse, ProfileInput, SIPPlanItem


def _monthly_sip_for_goal(target_amount: float, years: int, expected_return: float) -> float:
    months = years * 12
    monthly_rate = expected_return / 12
    growth_factor = (1 + monthly_rate) ** months
    return target_amount * monthly_rate / max(0.0001, (growth_factor - 1))


def _allocation_by_risk(risk: str) -> AssetAllocation:
    mapping = {
        "conservative": AssetAllocation(equity=35, debt=45, gold=10, cash=10),
        "balanced": AssetAllocation(equity=55, debt=30, gold=10, cash=5),
        "aggressive": AssetAllocation(equity=75, debt=15, gold=5, cash=5),
    }
    return mapping[risk]


def build_fire_roadmap(profile: ProfileInput) -> PlannerResponse:
    expected_return_map = {
        "conservative": 0.09,
        "balanced": 0.11,
        "aggressive": 0.13,
    }
    expected_return = expected_return_map[profile.risk_appetite]

    plan_items: list[SIPPlanItem] = []
    total_sip = 0.0
    for goal in profile.goals:
        sip = _monthly_sip_for_goal(goal.target_amount, goal.years_to_goal, expected_return)
        total_sip += sip
        plan_items.append(
            SIPPlanItem(
                goal_name=goal.name,
                monthly_sip=round(sip, 2),
                expected_corpus=round(goal.target_amount, 2),
                years_to_goal=goal.years_to_goal,
            )
        )

    emergency_target = round(profile.monthly_expenses * 6, 2)
    insurance_needed = profile.annual_salary * 15
    insurance_gap = round(max(0.0, insurance_needed - profile.annual_insurance_cover), 2)
    monthly_roadmap = [
        "Month 1-2: Build emergency fund and complete insurance coverage.",
        "Month 3-4: Start SIPs goal-wise and automate investments right after salary day.",
        "Month 5-6: Rebalance to target allocation and reduce high-interest debt.",
        "Month 7+: Increase SIP by 5-10% after every salary hike.",
    ]

    return PlannerResponse(
        total_monthly_sip=round(total_sip, 2),
        asset_allocation=_allocation_by_risk(profile.risk_appetite),
        emergency_fund_target=emergency_target,
        insurance_gap=insurance_gap,
        monthly_roadmap=monthly_roadmap,
        goals=plan_items,
    )
