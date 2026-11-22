
import math


def get_valid_number(value):
    if value is None:
        return None

    try:
        number = float(value)

        if not math.isfinite(number):
            return None

        return number

    except (TypeError, ValueError):
        return None


def evaluate_metrics(company_data):

    score = 0
    insights = []

    pe = get_valid_number(
        company_data.get("pe_ratio")
    )

    revenue = get_valid_number(
        company_data.get("revenue")
    )

    # --------------------
    # Valuation
    # --------------------

    if pe is not None and pe > 0:

        if pe < 15:
            valuation = "Potentially Undervalued"
            score += 3
            insights.append(
                "Low P/E ratio relative to the configured thresholds"
            )

        elif pe < 35:
            valuation = "Fairly Valued"
            score += 2
            insights.append(
                "P/E ratio falls within the configured middle range"
            )

        else:
            valuation = "Premium Valuation"
            score += 1
            insights.append(
                "High P/E ratio; valuation requires further examination"
            )

    else:
        valuation = "Unknown"

        insights.append(
            "Valuation cannot be assessed using the available P/E data"
        )

    # --------------------
    # Revenue Scale
    # --------------------

    if revenue is not None and revenue >= 0:

        if revenue > 100_000_000_000:
            growth = "Large Revenue Scale"
            score += 3

            insights.append(
                "Company has a large reported revenue base"
            )

        elif revenue > 10_000_000_000:
            growth = "Medium Revenue Scale"
            score += 2

            insights.append(
                "Company has a medium reported revenue base"
            )

        else:
            growth = "Smaller Revenue Scale"
            score += 1

            insights.append(
                "Company has a smaller reported revenue base"
            )

    else:
        growth = "Unknown"

        insights.append(
            "Revenue scale cannot be assessed using the available data"
        )

    # --------------------
    # Valuation-Based Risk Indicator
    # --------------------

    if pe is not None and pe > 0:

        if pe > 50:
            risk = "High"

        elif pe > 25:
            risk = "Medium"

        else:
            risk = "Low"

    else:
        risk = "Unknown"

    return {
        "score": score,
        "valuation": valuation,
        "growth": growth,
        "risk": risk,
        "insights": insights
    }
