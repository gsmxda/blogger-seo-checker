import requests
import xml.etree.ElementTree as ET

SITEMAP_URL = "https://www.gsmhelpful.com/sitemap.xml"

def get_urls_from_sitemap(sitemap_url):
    print(f"Fetching sitemap from: {sitemap_url}")
    try:
        response = requests.get(sitemap_url)
        if response.status_code != 200:
            print("Failed to fetch sitemap.")
            return []
        
        root = ET.fromstring(response.content)
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
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code >= 400:
                broken_links.append(f"{url} (Status: {res.status_code})")
                print(f"[BROKEN] {url} - Status: {res.status_code}")
            else:
                print(f"[OK] {url}")
        except Exception as e:
            broken_links.append(f"{url} (Error: {e})")
            print(f"[ERROR] {url} - {e}")
            
    return broken_links

if __name__ == "__main__":
    urls = get_urls_from_sitemap(SITEMAP_URL)
    if urls:
        broken = check_links(urls)
        if broken:
            print(f"\nFound {len(broken)} broken links!")
            # Broken links ko file mein save kar rahe hain taaki email mein bhej sakein
            with open("broken_links.txt", "w") as f:
                f.write("\n".join(broken))
            exit(1)
        else:
            print("\nAll links are healthy!")
            with open("broken_links.txt", "w") as f:
                f.write("No broken links found. All links are healthy!")
    else:
        print("No URLs found to check.")
        with open("broken_links.txt", "w") as f:
            f.write("Could not fetch sitemap or no URLs found.")
