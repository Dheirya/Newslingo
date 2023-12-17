import concurrent.futures
import feedparser
import random
import re

rss_feeds = {
    "Trending": [
        "http://rss.cnn.com/rss/cnn_topstories.rss",
        "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
        "https://moxie.foxnews.com/google-publisher/latest.xml",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "http://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
    ],
    "World": [
        "http://rss.cnn.com/rss/cnn_world.rss",
        "https://moxie.foxnews.com/google-publisher/world.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "http://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362",
    ],
    "US": [
        "http://rss.cnn.com/rss/cnn_us.rss",
        "https://moxie.foxnews.com/google-publisher/us.xml",
        "http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
        "https://timesofindia.indiatimes.com/rssfeeds_us/72258322.cms",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15837362",
    ],
    "Business": [
        "http://rss.cnn.com/rss/money_latest.rss",
        "http://feeds.bbci.co.uk/news/business/rss.xml",
        "http://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147",
    ],
    "Political": [
        "http://rss.cnn.com/rss/cnn_allpolitics.rss",
        "https://moxie.foxnews.com/google-publisher/politics.xml",
        "http://feeds.bbci.co.uk/news/politics/rss.xml",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000113",
    ],
    "Opinion": [
        "https://moxie.foxnews.com/google-publisher/opinion.xml",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100370673",
    ],
    "Technology": [
        "http://rss.cnn.com/rss/cnn_tech.rss",
        "https://moxie.foxnews.com/google-publisher/tech.xml",
        "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "http://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910",
    ],
    "Science": [
        "https://moxie.foxnews.com/google-publisher/science.xml",
        "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "http://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms",
    ],
    "Sports": [
        "https://moxie.foxnews.com/google-publisher/sports.xml",
        "http://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
    ],
    "Health": [
        "http://rss.cnn.com/rss/cnn_health.rss",
        "https://news.un.org/feed/subscribe/en/news/topic/health/feed/rss.xml",
        "https://moxie.foxnews.com/google-publisher/health.xml",
        "http://feeds.bbci.co.uk/news/health/rss.xml",
        "http://timesofindia.indiatimes.com/rssfeeds/2886704.cms",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000108",
    ],
    "Travel": [
        "http://rss.cnn.com/rss/cnn_travel.rss",
        "https://moxie.foxnews.com/google-publisher/travel.xml",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000739",
    ],
    "Arts": [
        "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
    ],
    "Entertainment": [
        "http://rss.cnn.com/rss/cnn_showbiz.rss",
        "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
        "http://timesofindia.indiatimes.com/rssfeeds/1081479906.cms",
    ],
}
rss_feed_urls_by_source = {source: [rss_feed_url for rss_feed_url in rss_feeds[category] if re.search(r'://(.*?)/', rss_feed_url).group(1) == source] for category, sources in rss_feeds.items() for source in sources}


def fetch_articles_from_category(category, articles_per_source=6, given_source="All"):
    if category in rss_feeds:
        selected_sources = rss_feeds[category]
        if given_source != "All":
            selected_sources = [rss_feed_url for rss_feed_url in selected_sources if re.search(r'://(.*?)/', rss_feed_url).group(1) == given_source]
    else:
        raise ValueError(f"Category '{category}' not found in rss_feeds")
    all_headlines = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_articles_from_source, rss_feed_url, articles_per_source) for rss_feed_url in selected_sources]
        concurrent.futures.wait(futures)
        for future in futures:
            all_headlines.extend(future.result())
    random.shuffle(all_headlines)
    return all_headlines


def fetch_articles_from_source(rss_feed_url, articles_per_source):
    num_entries, feed = get_feed_entries(rss_feed_url)
    num_selected = min(articles_per_source, num_entries)
    random_indices = random.sample(range(num_entries), num_selected)
    source_headlines = []
    for index in random_indices:
        entry = feed.entries[index]
        headline_data = {
            "title": entry.get("title"),
            "link": entry.get("link"),
            "description": entry.get("summary"),
            "source": re.search(r'://(.*?)/', rss_feed_url).group(1)
        }
        source_headlines.append(headline_data)
    return source_headlines


def get_feed_entries(rss_feed_url):
    feed = feedparser.parse(rss_feed_url)
    num_entries = len(feed.entries)
    return num_entries, feed


def get_selected_category_and_categories(request):
    categories = ["Trending", "World", "US", "Business", "Political", "Opinion", "Technology", "Science", "Sports", "Health", "Travel", "Arts", "Entertainment"]
    selected_category = request.GET.get('category', 'Trending')
    return selected_category, categories


def get_selected_source(request):
    source = request.GET.get('source', 'All')
    return source
