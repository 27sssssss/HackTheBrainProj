import feedparser
def get_data_disasters():
    url = "https://www.gdacs.org/xml/rss.xml" #url from where we take info
    feed = feedparser.parse(url)
    results = []
    for entry in feed.entries[:10]:
        results.append({
            "title" : entry.title,
            "summary": entry.summary,
            "date": entry.date,
            "link": entry.link
        })
    return results