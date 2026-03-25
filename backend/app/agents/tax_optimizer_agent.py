from __future__ import annotations

from app.models.schemas import TaxInput, TaxRegimeResult, TaxResponse


def _calc_tax_old_regime(taxable_income: float) -> float:
    slabs = [
        (250000, 0.0),
        (250000, 0.05),
        (500000, 0.20),
    ]
    tax = 0.0
    remaining = taxable_income

    for slab_amount, rate in slabs:
        taxable_at_rate = min(remaining, slab_amount)
        tax += taxable_at_rate * rate
        remaining -= taxable_at_rate
        if remaining <= 0:
            break

    if remaining > 0:
        tax += remaining * 0.30
    return tax


def _calc_tax_new_regime(taxable_income: float) -> float:
    slabs = [
        (400000, 0.0),
        (400000, 0.05),
        (400000, 0.10),
        (400000, 0.15),
        (400000, 0.20),
        (400000, 0.25),
    ]
    tax = 0.0
    remaining = taxable_income

    for slab_amount, rate in slabs:
        taxable_at_rate = min(remaining, slab_amount)
        tax += taxable_at_rate * rate
        remaining -= taxable_at_rate
        if remaining <= 0:
            break

    if remaining > 0:
        tax += remaining * 0.30
    return tax


def _build_result(taxable_income: float, base_tax: float) -> TaxRegimeResult:
    cess = base_tax * 0.04
    return TaxRegimeResult(
        taxable_income=round(taxable_income, 2),
        tax_before_cess=round(base_tax, 2),
        cess=round(cess, 2),
        total_tax=round(base_tax + cess, 2),
    )


def compare_tax_regimes(payload: TaxInput) -> TaxResponse:
    total_old_deductions = min(
        payload.section_80c + payload.section_80d + payload.hra_exemption + payload.home_loan_interest + payload.other_deductions,
        payload.annual_salary,
    )
    old_taxable_income = max(0.0, payload.annual_salary - total_old_deductions)
    new_standard_deduction = 75000.0
    new_taxable_income = max(0.0, payload.annual_salary - new_standard_deduction)

    old_result = _build_result(old_taxable_income, _calc_tax_old_regime(old_taxable_income))
    new_result = _build_result(new_taxable_income, _calc_tax_new_regime(new_taxable_income))

    if old_result.total_tax < new_result.total_tax:
        better_regime = "old"
        tax_saved = new_result.total_tax - old_result.total_tax
    elif new_result.total_tax < old_result.total_tax:
        better_regime = "new"
        tax_saved = old_result.total_tax - new_result.total_tax
    else:
        better_regime = "same"
        tax_saved = 0.0

    suggestions = [
        "Max out 80C via EPF, ELSS, PPF, or life insurance premium.",
        "Use NPS under 80CCD(1B) for additional tax benefit.",
        "Track HRA exemption with valid rent receipts.",
        "For salaried users, compare old vs new regime every April.",
    ]

    return TaxResponse(
        old_regime=old_result,
        new_regime=new_result,
        better_regime=better_regime,
        tax_saved=round(tax_saved, 2),
        suggestions=suggestions,
    )
