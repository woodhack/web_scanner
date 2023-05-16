import csv
import socket
import ipaddress
import requests
from bs4 import BeautifulSoup
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
]

def get_ip_addresses(url):
    try:
        domain = url.split('//')[1].split('/')[0]
        ip_addresses = []
        for addr in socket.getaddrinfo(domain, 80):
            if addr[0] == socket.AF_INET:
                ip_addresses.append(addr[4][0])
        ip_addresses = list(set(ip_addresses))
        ip_addresses.sort()
        return ip_addresses
    except socket.gaierror:
        return []

def scrape_website(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get title
        title = soup.title.string.strip() if soup.title else ''

        # Get keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = keywords['content'].strip() if keywords else ''

        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc['content'].strip() if meta_desc else ''

        # Get logo URL
        logo_url = soup.find('link', attrs={'rel': 'icon'})
        logo_url = logo_url['href'].strip() if logo_url else ''

        # Get IP addresses
        ip_addresses = get_ip_addresses(url)

        # Get social media links
        social_media_links = {
            'linkedin': '',
            'twitter': '',
            'facebook': '',
            'instagram': ''
        }
        for link in soup.find_all('a'):
            href = link.get('href', '').lower()
            if 'linkedin' in href:
                social_media_links['linkedin'] = href
            elif 'twitter' in href:
                social_media_links['twitter'] = href
            elif 'facebook' in href:
                social_media_links['facebook'] = href
            elif 'instagram' in href:
                social_media_links['instagram'] = href

        # Return results as a dictionary
        return {
            'url': url,
            'title': title,
            'keywords': keywords,
            'meta_desc': meta_desc,
            'logo_url': logo_url,
            'ip_addresses': ','.join(ip_addresses),
            'linkedin': social_media_links['linkedin'],
            'twitter': social_media_links['twitter'],
            'facebook': social_media_links['facebook'],
            'instagram': social_media_links['instagram']
        }

    except Exception as e:
        print(f"Error scraping website: {e}")
        return None


if __name__ == '__main__':
    # Read input CSV file
    with open('input.csv', 'r') as f:
        reader = csv.reader(f)
        urls = [row[0] for row in reader]

    # Scrape websites
    with open('output.csv', 'w', newline='', encoding='utf-8') as f:  # Open output file outside the loop
        writer = csv.DictWriter(f, fieldnames=['url', 'title', 'keywords', 'meta_desc', 'logo_url', 'ip_addresses', 'linkedin', 'twitter', 'facebook', 'instagram'])
        writer.writeheader()
        for i, url in enumerate(urls, start=1):
            print(f"Processing website {i}/{len(urls)}: {url}")
            result = scrape_website(url)
            if result is not None:
                writer.writerow(result)  # Write result to output file immediately after scraping

    print(f"Scraped {len(urls)} website(s) and saved results to output.csv")
