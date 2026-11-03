"""Synthetic comparison contracts, authored independently of private code."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass(frozen=True)
class Source:
    document: str
    section: str
    field: str
    def __post_init__(self):
        if not all((self.document.strip(), self.section.strip(), self.field.strip())):
            raise ValueError("source provenance required")

@dataclass(frozen=True)
class Finding:
    status: str
    reason: str
    left: Source
    right: Source
    delta: str | None = None

def money(value):
    result = Decimal(str(value))
    if not result.is_finite() or result < 0: raise ValueError("finite nonnegative amount required")
    return result

def compare_price(left, right, left_currency, right_currency, *, tolerance, sources):
    allowed = money(tolerance)
    if left is None or right is None or not left_currency or not right_currency:
        return Finding("UNVERIFIABLE", "missing amount or currency", *sources)
    a, b = money(left), money(right)
    if left_currency.upper() != right_currency.upper():
        return Finding("REVIEW_REQUIRED", "currency mismatch; no conversion performed", *sources)
    delta = b - a
    return Finding("CONFIRMED", "outside tolerance" if abs(delta) > allowed else "within tolerance", *sources, str(delta))

def compare_dates(left, right, *, tolerance_days):
    if type(tolerance_days) is not int or tolerance_days < 0: raise ValueError("nonnegative integer tolerance required")
    if left is None or right is None: return "UNVERIFIABLE"
    delta = (date.fromisoformat(right) - date.fromisoformat(left)).days
    return "OUTSIDE_TOLERANCE" if abs(delta) > tolerance_days else "WITHIN_TOLERANCE"
