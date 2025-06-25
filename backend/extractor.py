import feedparser
def get_data_disasters():
    url = "https://www.gdacs.org/xml/rss.xml" 
    feed = feedparser.parse(url)
    results = []
    for entry in feed.entries[:15]:
        results.append({
            "title" : entry.title,
            "summary": entry.summary,
            "date": entry.published,
            "link": entry.link
        })
    return results