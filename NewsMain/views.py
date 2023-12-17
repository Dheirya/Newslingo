from .rss_fetch import fetch_articles_from_category, get_selected_category_and_categories, get_selected_source
from django.shortcuts import render
from .scraper import scrape
import asyncio
import httpx
import json
import re

language_codes = {'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Italian': 'it', 'Danish': 'nl', 'Latin': 'la', 'Norwegian': 'no', 'Swedish': 'sv', 'Portuguese': 'pt'}


async def get_articles(selected_category, source):
    select = 6 if source == "All" else 8
    articles = await asyncio.to_thread(fetch_articles_from_category, category=selected_category, articles_per_source=select, given_source=source)
    return articles


async def translate_words(client, words, target_language):
    query = '%0A'.join(words)
    response = await client.get(f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={query}')
    translations = response.json()[0]
    translated = []
    if translations:
        for translation in translations:
            translated.append(translation[0].strip())
    return translated


async def process_paragraph(client, paragraph, target_language, freq):
    words = re.findall(r'<.*?>|[\w\']+', paragraph)
    translated_dict = {}
    word_counter = 0
    words_to_translate = []
    for i, word in enumerate(words):
        if not re.match(r'<.*?>', word) and (len(word) > 1 or word == 'I'):
            word_counter += 1
            if word_counter % freq == 0:
                if word not in translated_dict:
                    words_to_translate.append(word)
                else:
                    word_counter -= 1
    translations = await translate_words(client, words_to_translate, target_language)
    for word, translation in zip(words_to_translate, translations):
        if translation != word:
            paragraph = re.sub(r'\b{}\b(?![^<>]*>)'.format(re.escape(word)), f"<mark translation='{word}'>{translation.lower()}</mark>", paragraph, freq)
            translated_dict[word] = {"translation": translation, "word": word, "language": target_language}
    return paragraph, translated_dict


async def article(request):
    selected_category, categories = get_selected_category_and_categories(request)
    selected_article = request.GET.get('link')
    data = scrape(selected_article)
    language = request.COOKIES.get('languages', 'Spanish')
    language_code = language_codes.get(language, 'es')
    freq = int(request.COOKIES.get('frequency', 15))
    if freq < 10:
        freq = 10
    if freq > 95:
        freq = 95
    autosave = bool(request.COOKIES.get('autosave', True))
    async with httpx.AsyncClient() as client:
        translated_paragraph, translations_dict = await process_paragraph(client, data['content'], language_code, freq)
    if autosave:
        return render(request, 'NewsMain/article.html', {'categories': categories, 'selected_category': selected_category, 'title': data['title'], 'content': translated_paragraph, 'type': data['type'], 'url': selected_article, 'autosave_list': json.dumps(translations_dict)})
    return render(request, 'NewsMain/article.html', {'categories': categories, 'selected_category': selected_category, 'title': data['title'], 'content': translated_paragraph, 'type': data['type'], 'url': selected_article})


async def index(request):
    source_dropdown = {
        "Trending": {
            "CNN": "rss.cnn.com",
            "UN": "news.un.org",
            "FoxNews": "moxie.foxnews.com",
            "BBC": "feeds.bbci.co.uk",
            "CNBC": "search.cnbc.com",
            "Times of India": "timesofindia.indiatimes.com"
        },
        "World": {
            "CNN": "rss.cnn.com",
            "FoxNews": "moxie.foxnews.com",
            "BBC": "feeds.bbci.co.uk",
            "CNBC": "search.cnbc.com",
            "Times of India": "timesofindia.indiatimes.com"
        },
        "US": {
            "CNN": "rss.cnn.com",
            "FoxNews": "moxie.foxnews.com",
            "BBC": "feeds.bbci.co.uk",
            "CNBC": "search.cnbc.com",
            "Times of India": "timesofindia.indiatimes.com"
        },
        "Business": {
            "CNN": "rss.cnn.com",
            "BBC": "feeds.bbci.co.uk",
            "CNBC": "search.cnbc.com",
            "Times of India": "timesofindia.indiatimes.com"
        },
        "Political": {
            "CNN": "rss.cnn.com",
            "FoxNews": "moxie.foxnews.com",
            "BBC": "feeds.bbci.co.uk",
            "CNBC": "search.cnbc.com",
        },
        "Opinion": {
            "FoxNews": "moxie.foxnews.com",
            "CNBC": "search.cnbc.com",
        },
        "Technology": {
            "CNN": "rss.cnn.com",
            "FoxNews": "moxie.foxnews.com",
            "BBC": "feeds.bbci.co.uk",
            "CNBC": "search.cnbc.com",
            "Times of India": "timesofindia.indiatimes.com"
        },
        "Science": {
            "FoxNews": "moxie.foxnews.com",
            "BBC": "feeds.bbci.co.uk",
            "Times of India": "timesofindia.indiatimes.com"
        },
        "Sports": {
            "FoxNews": "moxie.foxnews.com",
            "Times of India": "timesofindia.indiatimes.com"
        },
        "Health": {
            "CNN": "rss.cnn.com",
            "UN": "news.un.org",
            "FoxNews": "moxie.foxnews.com",
            "BBC": "feeds.bbci.co.uk",
            "CNBC": "search.cnbc.com",
            "Times of India": "timesofindia.indiatimes.com"
        },
        "Travel": {
            "CNN": "rss.cnn.com",
            "FoxNews": "moxie.foxnews.com",
            "CNBC": "search.cnbc.com",
        },
        "Arts": {
            "BBC": "feeds.bbci.co.uk",
        },
        "Entertainment": {
            "CNN": "rss.cnn.com",
            "BBC": "feeds.bbci.co.uk",
            "Times of India": "timesofindia.indiatimes.com"
        },
    }
    selected_category, categories = get_selected_category_and_categories(request)
    source = get_selected_source(request)
    articles = await get_articles(selected_category, source)
    return render(request, 'NewsMain/index.html', {'categories': categories, 'given_source': source, 'selected_category': selected_category, 'articles': articles, 'dropdown': source_dropdown[selected_category]})


async def list(request):
    selected_category, categories = get_selected_category_and_categories(request)
    return render(request, 'NewsMain/list.html', {'categories': categories})
