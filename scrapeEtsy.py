import requests
from bs4 import BeautifulSoup

# Define the search URL and user agent string
base_url = 'https://www.etsy.com'
search_path = '/search?q=budget+planner'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

# Set the headers to include the user agent
headers = {'User-Agent': user_agent}

# Define a function to scrape the listings from a single page
def scrape_listings(url):
    # Send a request to the search page with the headers
    response = requests.get(url, headers=headers)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all of the product listings on the page
    page_listings = soup.find_all('div', class_='v2-listing-card')

    # Count the number of listings found on the page
    num_listings = len(page_listings)

    # Loop through each listing and extract the desired data
    for listing in page_listings:
        # Extract the product title
        title = listing.find('h3', class_='v2-listing-card__title').text.strip()

        # Extract the product price
        price_value = listing.select_one('.wt-mr-xs-0 .lc-price .lc-price .currency-value').text.strip()
        currency_symbol = listing.select_one('.wt-mr-xs-0 .lc-price .lc-price .currency-symbol').text.strip()
        price = f'{price_value} - {currency_symbol}'

        # Extract the product rating, if available
        rating_element = listing.find('div', class_='wt-pr-xs-1')
        rating = rating_element.find('span', class_='screen-reader-only').text.strip() if rating_element else 'N/A'

        # Extract the product URL, if available
        url_element = listing.find('a', class_='listing-link')
        url = url_element['href'] if url_element else ''

        
        # Print out the data for this listing
        print(f'Title: {title}')
        print(f'Price: {price}')
        print(f'Rating: {rating}')
        print(f'URL: {base_url}{url}')
        print('------------------------')

    # Print the number of listings found on the page
    print(f'Number of listings found: {num_listings}\n')

    return num_listings

# Loop over the search results pages and scrape the listings from each page
page_number = 1
total_listings = 0
while True:
    # Construct the URL for the current page of search results
    search_url = f'{base_url}{search_path}&page={page_number}&limit=100'

    # Send a request to the search page with the headers
    response = requests.get(search_url, headers=headers)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all of the product listings on the page
    listings = soup.find_all('div', class_='v2-listing-card')

    # If no listings are found, break out of the loop
    if not listings:
        break

        # Scrape the listings from the current page and update the total count
    num_listings = scrape_listings(search_url)
    total_listings += num_listings

    # If we have scraped 10 pages, break out of the loop

    # Move to the next page of search results
    page_number += 1

# Print the total number of listings found
print(f'Total number of listings found: {total_listings}')

