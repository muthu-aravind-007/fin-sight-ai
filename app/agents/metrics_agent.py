def evaluate_metrics(company_data):

    score = 0

    pe = company_data.get("pe_ratio")
    revenue = company_data.get("revenue")

    insights = []

    # --------------------
    # Valuation
    # --------------------

    if pe:

        if pe < 15:
            valuation = "Undervalued"
            score += 3
            insights.append(
                "Attractive valuation"
            )

        elif pe < 35:
            valuation = "Fairly Valued"
            score += 2
            insights.append(
                "Reasonable valuation"
            )

        else:
            valuation = "Overvalued"
            score += 1
            insights.append(
                "Premium valuation"
            )

    else:
        valuation = "Unknown"

    # --------------------
    # Growth
    # --------------------

    if revenue:

        if revenue > 100_000_000_000:

            growth = "Strong"

            score += 3

            insights.append(
                "Very strong revenue"
            )

        elif revenue > 10_000_000_000:

            growth = "Moderate"

            score += 2

            insights.append(
                "Healthy revenue"
            )

        else:

            growth = "Weak"

            score += 1

            insights.append(
                "Limited revenue scale"
            )

    else:
        growth = "Unknown"

    # --------------------
    # Risk
    # --------------------

    if pe:

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