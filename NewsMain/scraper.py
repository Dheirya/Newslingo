from bs4 import BeautifulSoup
import requests


def foxNewsScraper(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_title = soup.find('h1', class_='headline')
        article_body_div = soup.find('div', class_='article-body')
        if article_title and article_body_div:
            article_title = article_title.get_text()
            article_paragraphs = article_body_div.find_all('p', recursive=False)
            article_content = "\n".join([f'<p>{p.get_text()}</p>' for p in article_paragraphs])
            cleaned_text = '\n'.join(' '.join(line.split()) for line in article_content.split('\n'))
            cleaned_text = '\n\n'.join(line.strip() for line in cleaned_text.split('\n\n'))
            return {"title": article_title, "content": cleaned_text}
        return {"title": "ERROR", "content": "Article text not found on the page. <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}
    return {"title": "ERROR", "content": "Failed to retrieve the webpage. Status code: " + str(response.status_code) + ". <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}


def cnbcNewsScraper(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_title = soup.find('h1')
        article_body_div = soup.find_all('div', {'class': 'group'})
        if article_title and article_body_div:
            article_title = article_title.get_text()
            article_paragraphs = []
            for div in article_body_div:
                paragraphs = div.find_all('p', recursive=True)
                article_paragraphs.extend(paragraphs)
            article_content = "\n".join([f'<p>{p.get_text()}</p>' for p in article_paragraphs])
            cleaned_text = '\n'.join(' '.join(line.split()) for line in article_content.split('\n'))
            cleaned_text = '\n\n'.join(line.strip() for line in cleaned_text.split('\n\n'))
            return {"title": article_title, "content": cleaned_text}
        return {"title": "ERROR", "content": "Article text not found on the page. <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}
    return {"title": "ERROR", "content": "Failed to retrieve the webpage. Status code: " + str(response.status_code) + ". <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}


def unNewsScraper(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_title = soup.find('h1')
        article_body_div = soup.find('div', class_='text-formatted')
        if article_title and article_body_div:
            article_title = article_title.get_text()
            article_paragraphs = article_body_div.find_all('p', recursive=False)
            article_content = "\n".join([f'<p>{p.get_text()}</p>' for p in article_paragraphs])
            cleaned_text = '\n'.join(' '.join(line.split()) for line in article_content.split('\n'))
            cleaned_text = '\n\n'.join(line.strip() for line in cleaned_text.split('\n\n'))
            return {"title": article_title, "content": cleaned_text}
        return {"title": "ERROR", "content": "Article text not found on the page. <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}
    return {"title": "ERROR", "content": "Failed to retrieve the webpage. Status code: " + str(response.status_code) + ". <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}


def bbcNewsScraper(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_title = soup.find('h1', id='main-heading')
        article_body_div = soup.find_all('div', {'data-component': 'text-block'})
        if article_title and article_body_div:
            article_title = article_title.get_text()
            article_paragraphs = []
            for div in article_body_div:
                paragraphs = div.find_all('p', recursive=True)
                article_paragraphs.extend(paragraphs)
            article_content = "\n".join([f'<p>{p.get_text()}</p>' for p in article_paragraphs])
            cleaned_text = '\n'.join(' '.join(line.split()) for line in article_content.split('\n'))
            cleaned_text = '\n\n'.join(line.strip() for line in cleaned_text.split('\n\n'))
            return {"title": article_title, "content": cleaned_text}
        return {"title": "ERROR", "content": "Article text not found on the page. <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}
    return {"title": "ERROR", "content": "Failed to retrieve the webpage. Status code: " + str(response.status_code) + ". <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}


def cnnNewsScraper(url):
    response = requests.get(url.replace('www.cnn.com', 'lite.cnn.com'))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_title = soup.find('h2', {'class': 'headline'})
        article_body_div = soup.find_all('article', {'class': 'article--lite'})
        if article_title and article_body_div:
            article_title = article_title.get_text()
            article_paragraphs = []
            for div in article_body_div:
                paragraphs = div.find_all('p', recursive=True)
                article_paragraphs.extend(paragraphs)
            article_content = "\n".join([f'<p>{p.get_text()}</p>' for p in article_paragraphs])
            cleaned_text = '\n'.join(' '.join(line.split()) for line in article_content.split('\n'))
            cleaned_text = '\n\n'.join(line.strip() for line in cleaned_text.split('\n\n'))
            return {"title": article_title, "content": cleaned_text}
        return {"title": "ERROR", "content": "Article text not found on the page. <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}
    return {"title": "ERROR", "content": "Failed to retrieve the webpage. Status code: " + str(response.status_code) + ". <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}


def indianNewsScraper(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_title = soup.find('h1', class_='HNMDR').find('span')
        article_body_div = soup.find('div', class_='_s30J')
        if article_title and article_body_div:
            article_title = article_title.get_text()
            article_content = article_body_div.get_text()
            cleaned_text = '\n'.join([f'<p>{line.strip()}</p>' for line in article_content.split('\n') if line.strip()])
            return {"title": article_title, "content": cleaned_text}
        return {"title": "ERROR", "content": "Article text not found on the page. <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}
    return {"title": "ERROR", "content": "Failed to retrieve the webpage. Status code: " + str(response.status_code) + ". <a href='javascript:window.location.href=window.location.href'>Reload</a> page or go <a href='/'>home</a>"}


def scrape(url):
    if "foxnews." in url:
        return {**foxNewsScraper(url), "type": "Fox"}
    elif "cnbc." in url:
        return {**cnbcNewsScraper(url), "type": "CNBC"}
    elif "un." in url:
        return {**unNewsScraper(url), "type": "UN"}
    elif "bbc." in url:
        return {**bbcNewsScraper(url), "type": "BBC"}
    elif "cnn." in url:
        return {**cnnNewsScraper(url), "type": "CNN"}
    elif "indiatimes." in url:
        return {**indianNewsScraper(url), "type": "Times of India"}
    else:
        return {"title": "ERROR", "content": "No scraper found for this website."}
