import socket
import ipaddress
import requests
from bs4 import BeautifulSoup

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
        response = requests.get(url)
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

        # Print results
        print(f"Title: {title}")
        print(f"Keywords: {keywords}")
        print(f"Meta Description: {meta_desc}")
        print(f"Logo URL: {logo_url}")
        print(f"IP Addresses: {ip_addresses}")
        print(f"Social Media Links: {social_media_links}")

    except Exception as e:
        print(f"Error scraping website: {e}")

if __name__ == '__main__':
    url = input("Enter a URL to scrape: ")
    scrape_website(url)
