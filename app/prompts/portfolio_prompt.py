def build_portfolio_prompt(
    companies,
    average_score,
    sectors
):

    return f"""
You are a professional portfolio analyst.

Portfolio Holdings:

{companies}

Average Portfolio Score:

{average_score}

Sector Allocation:

{sectors}

Generate:

1. Portfolio Strengths

2. Diversification Assessment

3. Risk Assessment

4. Sector Concentration Risks

5. Suggested Improvements

6. Final Portfolio Rating

Keep it concise and professional.
"""