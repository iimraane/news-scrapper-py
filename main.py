import requests
from bs4 import BeautifulSoup

# URL de Google News
url = 'https://news.google.com/home?hl=fr&gl=FR&ceid=FR:fr'

def scrape_google_news(url):
    # Envoyer une requête HTTP à l'URL
    response = requests.get(url)
    response.raise_for_status()  # Vérifier si la requête a réussi

    # Parser le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les articles
    news_data = []
    articles = soup.select('article')
    for article in articles:
        link_tag = article.select_one('a[href]')
        link = link_tag['href'] if link_tag else None
        if link:
            full_link = 'https://news.google.com' + link[1:] if link.startswith('./') else link
            news_data.append({'link': full_link})
    return news_data

def get_final_url(url):
    session = requests.Session()
    response = session.get(url, allow_redirects=True)
    response.raise_for_status()  # Vérifier si la requête a réussi
    return response.url, response.text

def get_article_title(url, html_content):
    # Parser le contenu HTML de la page de l'article
    soup = BeautifulSoup(html_content, 'html.parser')

    # Essayer plusieurs sélecteurs CSS pour trouver le titre de l'article
    title_tag = (soup.select_one('h1') or
                 soup.select_one('h2') or
                 soup.title)
    title = title_tag.text.strip() if title_tag else 'No Title'
    return title

def main():
    news_data = scrape_google_news(url)
    
    for news in news_data:
        final_url, html_content = get_final_url(news['link'])
        news['title'] = get_article_title(final_url, html_content)
        print(f"Title: {news['title']}")
        print(f"Link: {final_url}\n")

if __name__ == "__main__":
    main()
