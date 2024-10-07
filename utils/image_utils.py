import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_first_google_image(film):
    query = f"affiche officiel film {film}"
    search_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_query}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    images = soup.find_all('img')
    
    if images:
        first_image_url = images[1]['src']
        return first_image_url
    else:
        return None
