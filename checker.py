import requests
import xml.etree.ElementTree as ET

# Apne Blogger blog ka sitemap URL yahan dalein
SITEMAP_URL = "https://www.gsmhelpful.com/sitemap.xml"

def get_urls_from_sitemap(sitemap_url):
    print(f"Fetching sitemap from: {sitemap_url}")
    try:
        response = requests.get(sitemap_url)
        if response.status_code != 200:
            print("Failed to fetch sitemap.")
            return []
        
        # Parse XML sitemap
        root = ET.fromstring(response.content)
        # Handle XML namespace if present
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        return urls
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
        return []

def check_links(urls):
    broken_links = []
    print(f"Checking {len(urls)} URLs...")
    for url in urls:
        try:
            # User-agent lagana zaroori hai taaki website block na kare
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code >= 400:
                broken_links.append((url, res.status_code))
                print(f"[BROKEN] {url} - Status: {res.status_code}")
            else:
                print(f"[OK] {url}")
        except Exception as e:
            broken_links.append((url, str(e)))
            print(f"[ERROR] {url} - {e}")
            
    return broken_links

if __name__ == "__main__":
    urls = get_urls_from_sitemap(SITEMAP_URL)
    if urls:
        broken = check_links(urls)
        if broken:
            print(f"\nFound {len(broken)} broken links!")
            exit(1) # Agar broken links milte hain toh workflow fail dikhayega (notification ke liye)
        else:
            print("\nAll links are healthy!")
    else:
        print("No URLs found to check.")
