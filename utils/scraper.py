import requests
from bs4 import BeautifulSoup

def scrape_education_news():
    url = "https://www.bbc.com/news/education"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = soup.find_all("h3")

    return [h.text for h in headlines[:5]]
