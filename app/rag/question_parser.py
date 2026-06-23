import re


def parse_question(question):

    result = {
        "quarters": [],
        "comparison_mode": False
    }

    quarters = re.findall(
        r"Q[1-4](?:[\s\-]*FY)?[\s\-]*\d{4}",
        question,
        flags=re.IGNORECASE
    )

    normalized_quarters = []

    for q in quarters:

        q = q.upper().replace("-", " ")

        q = q.replace("FY", "")

        q = " ".join(q.split())

        normalized_quarters.append(q)

    result["quarters"] = normalized_quarters

    q = question.lower()

    if any(
        x in q
        for x in [
            "compare",
            "vs",
            "versus",
            "difference"
        ]
    ):
        result["comparison_mode"] = True

    return result