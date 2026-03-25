from app.agents.tax_optimizer_agent import compare_tax_regimes
from app.models.schemas import TaxInput, TaxWizardInput, TaxWizardResponse


def run_tax_wizard(payload: TaxWizardInput) -> TaxWizardResponse:
    missing = []
    if payload.section_80c < 150000:
        missing.append("Section 80C limit not fully utilized.")
    if payload.section_80d <= 0:
        missing.append("Section 80D health insurance deduction missing.")
    if payload.hra_exemption <= 0:
        missing.append("HRA exemption not claimed or not optimized.")
    if payload.home_loan_interest <= 0:
        missing.append("Home loan interest deduction not claimed (if applicable).")

    base = TaxInput(
        annual_salary=payload.annual_salary,
        section_80c=payload.section_80c,
        section_80d=payload.section_80d,
        hra_exemption=payload.hra_exemption,
        home_loan_interest=payload.home_loan_interest,
        other_deductions=payload.other_deductions,
    )
    comparison = compare_tax_regimes(base)

    ranked_options = [
        "Low risk: EPF/PPF contribution top-up under 80C.",
        "Moderate risk: ELSS allocation for tax + long-term growth.",
        "Liquidity-aware: Keep emergency corpus before locking long-tenure products.",
        "Additional benefit: NPS (80CCD(1B)) for extra deduction.",
    ]

    return TaxWizardResponse(
        missing_deductions=missing,
        old_vs_new_summary=comparison,
        ranked_tax_saving_options=ranked_options,
    )
