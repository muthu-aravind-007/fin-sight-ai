import feedparser

def get_company_news(company_name: str):

    query = company_name.replace(" ", "+")

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