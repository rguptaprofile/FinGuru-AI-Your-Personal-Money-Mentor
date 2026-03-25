from app.models.schemas import CouplesPlannerInput, CouplesPlannerResponse


def build_couples_plan(payload: CouplesPlannerInput) -> CouplesPlannerResponse:
    p1 = payload.partner_one
    p2 = payload.partner_two

    combined_income = p1.annual_salary + p2.annual_salary
    combined_monthly_income = combined_income / 12
    combined_monthly_expenses = p1.monthly_expenses + p2.monthly_expenses
    combined_monthly_emi = p1.monthly_emi + p2.monthly_emi
    monthly_surplus = max(0.0, combined_monthly_income - combined_monthly_expenses - combined_monthly_emi)

    income_share_1 = p1.annual_salary / max(1.0, combined_income)
    income_share_2 = p2.annual_salary / max(1.0, combined_income)

    sip_target = payload.combined_goal_sip_target if payload.combined_goal_sip_target > 0 else monthly_surplus * 0.5
    sip_split = {
        p1.name: round(sip_target * income_share_1, 2),
        p2.name: round(sip_target * income_share_2, 2),
    }

    notes = [
        "Compare HRA claim optimization across both partners before filing returns.",
        "Use NPS and 80C limits efficiently at individual level.",
        "Review joint vs individual term insurance for dependent liabilities.",
        "Track combined net worth monthly for shared goals.",
    ]

    return CouplesPlannerResponse(
        combined_annual_income=round(combined_income, 2),
        combined_monthly_surplus=round(monthly_surplus, 2),
        suggested_sip_split=sip_split,
        tax_optimization_notes=notes,
    )
