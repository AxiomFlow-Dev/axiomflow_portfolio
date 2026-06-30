import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# 1. Raw HTML Input Catalog
mock_html_page = """
<html>
    <head><title>Maroc Tech Sandbox Catalog</title></head>
    <body>
        <div class="shop-container">
            <article class="product-card">
                <h3 class="item-title"><a href="/items/1" title="Pro Laptop Core i7">Pro Laptop Core i7</a></h3>
                <p class="price-tag">£600.00</p>
            </article>
            <article class="product-card">
                <h3 class="item-title"><a href="/items/2" title="Gaming Screen 144Hz">Gaming Screen 144Hz</a></h3>
                <p class="price-tag">£220.50</p>
            </article>
            <article class="product-card">
                <h3 class="item-title"><a href="/items/3" title="Mechanical Keyboard RGB">Mechanical Keyboard RGB</a></h3>
                <p class="price-tag">£45.00</p>
            </article>
            <article class="product-card">
                <h3 class="item-title"><a href="/items/4" title="Wireless Performance Mouse">Wireless Performance Mouse</a></h3>
                <p class="price-tag">£32.10</p>
            </article>
        </div>
    </body>
</html>
"""

print("\n" + "="*65)
print(" 🚀 INTEL ENGINE v2.0: RUNNING MULTI-TRACK DATA PIPELINE")
print("="*65)

soup = BeautifulSoup(mock_html_page, "lxml")
extracted_items = []
products = soup.find_all("article", class_="product-card")

# 2. Parsing Loop with Glitch-Guard Defenses
for idx, product in enumerate(products, 1):
    try:
        title_tag = product.find("h3", class_="item-title").find("a")
        title = title_tag["title"] if title_tag else "Unknown Product"
        
        price_tag = product.find("p", class_="price-tag")
        if not price_tag:
            continue
            
        price_text = price_tag.text.strip()
        price_gbp = float(price_text.replace("£", ""))
        
        # Financial Transformation Math
        price_mad = round((price_gbp * 11.8) * 1.10, 2)
        
        extracted_items.append({
            "Item ID": f"TECH-{2026 + idx}",
            "Product Name": title,
            "Original Price": price_text,
            "Price_MAD_Numerical": price_mad,
            "Price (MAD + Tax)": f"{price_mad} DH"
        })
    except Exception as parse_error:
        print(f"⚠️ [Row {idx}] Skipped corrupted data block: {parse_error}")

# 3. DataFrame Core Compilation
df = pd.DataFrame(extracted_items)

# Sort items from highest price to lowest price for a professional graph layout
df = df.sort_values(by="Price_MAD_Numerical", ascending=True)

# Save Master Spreadsheet Data Matrix
df.to_excel("Market_Intel_Report.xlsx", index=False)

# 4. Executive Analytics Console Dashboard
print("\n📊 MANAGEMENT EXECUTIVE SUMMARY")
print("-" * 65)
total_val = df["Price_MAD_Numerical"].sum()
avg_price = df["Price_MAD_Numerical"].mean()
max_price = df["Price_MAD_Numerical"].max()

print(f"🔹 Total Value of Catalog Stock : {total_val:,.2f} DH")
print(f"🔹 Average Cost Per Item        : {avg_price:,.2f} DH")
print(f"🔹 Most Expensive Item Found    : {max_price:,.2f} DH")
print("-" * 65)

# 5. High-Attention Cosmetic Visualization Engine
print("\n🎨 Generating Visual Analytics Asset...")

# Set up canvas dimensions and style
plt.figure(figsize=(10, 6))
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Custom Requested Palette Map (Assign distinct corporate colors to item tiers)
custom_colors = ['#f1c40f', '#2ecc71', '#e74c3c', '#2980b9']  # Yellow, Light Green, Red, Blue

# Generate horizontal bar chart for high readability of product text strings
bars = plt.barh(df["Product Name"], df["Price_MAD_Numerical"], color=custom_colors, edgecolor='#2c3e50', height=0.6)

# Typography and Label Styling
plt.title("Market Intel Report: Product Competitor Pricing Matrix", fontsize=14, fontweight='bold', pad=20, color='#2c3e50')
plt.xlabel("Price in Moroccan Dirhams (MAD + 10% Tax)", fontsize=11, fontweight='bold', labelpad=12, color='#2c3e50')
plt.ylabel("Monitored Hardware Components", fontsize=11, fontweight='bold', labelpad=12, color='#2c3e50')

# Inject live data labels onto the end of each visual bar container
for bar in bars:
    width = bar.get_width()
    plt.text(width + 150, bar.get_y() + bar.get_height()/2, f'{width:,.2f} DH', 
             va='center', ha='left', fontsize=10, fontweight='bold', color='#34495e')

# Adjust layout padding so no elements compress or clip
plt.xlim(0, max_price * 1.18)
plt.tight_layout()

# Save analytical chart directly into your project root directory
chart_filename = "Market_Intel_Chart.png"
plt.savefig(chart_filename, dpi=300)
plt.close()

print(f"🏆 SUCCESS! Spreadsheet synchronized and visual chart saved as: {chart_filename}\n")