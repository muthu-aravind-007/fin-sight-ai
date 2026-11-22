import feedparser


def get_company_news(company_name: str):

    if not company_name or not company_name.strip():
        return []

    query = company_name.strip().replace(" ", "+")

    url = (
        f"https://news.google.com/rss/search?q={query}"
    )

    feed = feedparser.parse(url)

    news = []

    for entry in feed.entries[:5]:

        news.append(
            {
                "title": entry.title,
                "link": entry.link
            }
        )

    return news
