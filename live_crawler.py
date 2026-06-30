import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Europe"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, "lxml")

Country_Name = []

table = soup.find("table", class_="wikitable")

for row in table.find_all("tr"):
    # Find ALL links anywhere inside this specific row
    links = row.find_all("a")
    
    for link in links:
        # Get the 'title' attribute of the link (e.g., "Albania" or "Flag of Albania")
        title = link.get("title", "")
        text = link.text.strip()
        
        # If the link has text, and it's NOT a flag, and it's NOT an ISO code link
        if text and "Flag" not in title and "ISO" not in text and not text.startswith("["):
            print(f"Found: {text}")
            Country_Name.append(text)
            break # Found the country for this row! Move to the next row.

# Export sequence
df = pd.DataFrame({"European Countries": Country_Name})
df.to_excel("europe_countries.xlsx", index=False)
print(f"🎉 Process Complete! Saved {len(Country_Name)} countries to excel.")