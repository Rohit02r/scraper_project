from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Function to scrape website data, including metadata
def scrape_website(url):
    # Use Selenium for headless browsing
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
    except Exception as e:
        driver.quit()
        return {"error": str(e)}

    # Extract metadata
    metadata = {
        "title": soup.title.string if soup.title else "No title found",
        "description": soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else "No description found",
        "keywords": soup.find("meta", {"name": "keywords"})["content"] if soup.find("meta", {"name": "keywords"}) else "No keywords found",
        "author": soup.find("meta", {"name": "author"})["content"] if soup.find("meta", {"name": "author"}) else "No author found",
    }

    # Extract advanced data
    headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]
    hashtags = [tag.get_text(strip=True) for tag in soup.find_all('a') if tag.get_text().startswith('#')]
    links = [a['href'] for a in soup.find_all('a', href=True)]
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

    # Add timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "metadata": metadata,
        "headings": headings,
        "hashtags": hashtags,
        "links": links,
        "paragraphs": paragraphs,
        "timestamp": timestamp,
    }

# Home view
def home(request):
    return render(request, 'scraper/home.html')

# Scrape data and return as JSON
def scrape_data(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'No URL provided.'}, status=400)

    scraped_data = scrape_website(url)
    if 'error' in scraped_data:
        return JsonResponse(scraped_data, status=400)

    return JsonResponse(scraped_data)
