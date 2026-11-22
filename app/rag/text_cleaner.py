
import math
import re
from collections import Counter


WHITESPACE_RE = re.compile(r"\s+")

URL_RE = re.compile(
    r"(?:https?://|www\.)\S+",
    flags=re.IGNORECASE,
)

DOMAIN_RE = re.compile(
    r"\b[a-z0-9-]+(?:\.[a-z0-9-]+)+\b",
    flags=re.IGNORECASE,
)

NAVIGATION_RE = re.compile(
    r"\b("
    r"privacy policy|terms of service|contact us|contact|"
    r"sign in|sign up|my watchlists|watchlists|"
    r"market data|stock screener|top gainers|top losers|"
    r"market heatmap|earnings transcripts|popular stocks|"
    r"about us|all rights reserved"
    r")\b",
    flags=re.IGNORECASE,
)


def normalize_line(line):
    return WHITESPACE_RE.sub(" ", line).strip()


def _page_lines(document):
    return [
        normalize_line(line)
        for line in (document.page_content or "").splitlines()
        if normalize_line(line)
    ]


def _is_repeated_page_furniture(
    line,
    position,
    page_line_count,
    frequency,
    threshold,
):
    if frequency < threshold or len(line) < 8:
        return False

    boundary_size = max(
        3,
        math.ceil(page_line_count * 0.15),
    )

    near_boundary = (
        position < boundary_size
        or position >= page_line_count - boundary_size
    )

    if not near_boundary:
        return False

    if len(line.split()) <= 3 and line.endswith(":"):
        return False

    return True


def _looks_like_navigation_block(lines):
    if len(lines) < 5:
        return False

    short_line_ratio = sum(
        len(line.split()) <= 5 for line in lines
    ) / len(lines)

    navigation_signals = sum(
        bool(NAVIGATION_RE.search(line))
        for line in lines
    )

    link_signals = sum(
        bool(URL_RE.search(line) or DOMAIN_RE.search(line))
        for line in lines
    )

    return (
        short_line_ratio >= 0.60
        and (
            navigation_signals >= 3
            or (navigation_signals >= 2 and link_signals >= 1)
        )
    )


def _remove_trailing_navigation(lines):
    """
    Remove only a trailing block that looks like website navigation.
    Keep the transcript text preceding that block.
    """
    for start in range(len(lines)):
        candidate = lines[start:]

        if _looks_like_navigation_block(candidate):
            return lines[:start]

    return lines


def clean_documents(documents):
    """
    Clean extracted transcript pages while preserving their metadata.
    """
    if not documents:
        return []

    page_lines = [
        _page_lines(document)
        for document in documents
    ]

    boundary_lines = []

    for lines in page_lines:
        if not lines:
            continue

        boundary_size = max(
            3,
            math.ceil(len(lines) * 0.15),
        )

        boundary_lines.extend(lines[:boundary_size])
        boundary_lines.extend(lines[-boundary_size:])

    frequencies = Counter(
        line.casefold()
        for line in boundary_lines
        if len(line) >= 8
    )

    threshold = max(
        3,
        math.ceil(len(documents) * 0.30),
    )

    cleaned_documents = []

    for document, lines in zip(documents, page_lines):
        if not lines:
            continue

        kept_lines = []

        for position, line in enumerate(lines):
            if _is_repeated_page_furniture(
                line=line,
                position=position,
                page_line_count=len(lines),
                frequency=frequencies[line.casefold()],
                threshold=threshold,
            ):
                continue

            kept_lines.append(line)

        kept_lines = _remove_trailing_navigation(kept_lines)

        cleaned_text = "\n".join(kept_lines).strip()

        if not cleaned_text:
            continue

        document.page_content = cleaned_text
        cleaned_documents.append(document)

    return cleaned_documents
