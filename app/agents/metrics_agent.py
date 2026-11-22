
def evaluate_metrics(company_data):

    company_data = company_data or {}

    pe = get_valid_number(
        company_data.get("pe_ratio")
    )

    revenue = get_valid_number(
        company_data.get("revenue")
    )

    # --------------------
    # Valuation Indicator
    # --------------------

    if pe is not None and pe > 0:
        valuation = f"P/E ratio: {pe:.2f}"

        valuation_insight = (
            "P/E ratio is available. A valuation conclusion "
            "requires comparison with historical, industry, "
            "and earnings-growth data."
        )
    else:
        valuation = "Unknown"

        valuation_insight = (
            "Valuation cannot be assessed because valid P/E data "
            "is unavailable."
        )

    # --------------------
    # Revenue Scale
    # --------------------

    if revenue is not None and revenue >= 0:

        if revenue > 100_000_000_000:
            revenue_scale = "Large"

        elif revenue > 10_000_000_000:
            revenue_scale = "Medium"

        else:
            revenue_scale = "Small"

        revenue_insight = (
            f"Reported revenue indicates a {revenue_scale.lower()} "
            "revenue base. Revenue scale does not establish "
            "revenue growth or profitability."
        )

    else:
        revenue_scale = "Unknown"

        revenue_insight = (
            "Revenue scale cannot be assessed because valid "
            "revenue data is unavailable."
        )

    return {
        "score": None,
        "valuation": valuation,
        "growth": "Unknown",
        "revenue_scale": revenue_scale,
        "risk": "Not Assessed",
        "insights": [
            valuation_insight,
            revenue_insight,
            "Revenue growth requires historical revenue data.",
            "Comprehensive financial risk requires additional "
            "financial and operational metrics."
        ]
    }


def get_valid_number(value):

    if value is None:
        return None

    try:
        import math

        number = float(value)

        if not math.isfinite(number):
            return None

        return number

    except (TypeError, ValueError):
        return None
