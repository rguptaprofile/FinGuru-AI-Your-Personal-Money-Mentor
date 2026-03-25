from app.models.schemas import LifeEventInput, LifeEventResponse


def advise_on_life_event(payload: LifeEventInput) -> LifeEventResponse:
    event = payload.event_type
    amount = payload.amount

    common_steps = [
        "Protect emergency fund first (minimum 6 months expenses).",
        "Keep high-interest debt reduction as first financial priority.",
        "Invest surplus through diversified SIP + index strategy.",
    ]

    specific_steps = {
        "bonus": ["Use 40% for goals, 30% for debt prepayment, 30% for near-term liquidity."],
        "inheritance": ["Avoid lump-sum equity deployment; stagger over 6-12 months."],
        "marriage": ["Create joint budget, insurance review, and aligned goal SIP plan."],
        "new_baby": ["Start child goal SIP and increase health/life cover."],
        "job_change": ["Build 9-month emergency buffer before aggressive investing."],
    }

    if amount > 0:
        allocation = {
            "emergency_or_liquid": round(amount * 0.30, 2),
            "debt_reduction": round(amount * 0.25, 2),
            "long_term_investments": round(amount * 0.45, 2),
        }
    else:
        allocation = {"emergency_or_liquid": 0.0, "debt_reduction": 0.0, "long_term_investments": 0.0}

    return LifeEventResponse(
        event_type=event,
        action_plan=common_steps + specific_steps.get(event, []),
        suggested_allocation=allocation,
    )
