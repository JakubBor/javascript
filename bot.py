import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re

def extract_allocations(text):
    """
    Wyszukuje ciągi typu '40% spot XRP' lub '30% ETH' itp.
    """
    pattern = r'(\d{1,3})%\s+(spot\s+)?([A-Z]{2,6})'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    if not matches:
        return ["❌ Nie znaleziono alokacji w tekście."]

    allocations = []
    for match in matches:
        percent = match[0]
        coin = match[2].upper()
        allocations.append(f"{percent}% spot {coin}")

    return allocations

def check_news():
    url = "https://jakubbor.github.io/javascript/trw.html"  # <-- ZMIEŃ NA PRAWDZIWY URL

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        date = soup.find("time")
        content = soup.find("div", class_="article-body")  # ZMIEŃ, jeśli inna struktura

        print(f"\n🕓 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — Sprawdzanie wiadomości:")

        print("\n🗓️ Data wiadomości:")
        print(date.text.strip() if date else "Brak daty")

        print("\n📰 Treść wiadomości:")
        article_text = content.text.strip() if content else "Brak treści"
        print(article_text[:300] + "..." if len(article_text) > 300 else article_text)

        print("\n📊 Wykryte alokacje:")
        allocations = extract_allocations(article_text)
        for a in allocations:
            print(a)

    except Exception as e:
        print("❌ Błąd podczas pobierania wiadomości:", e)

# === Pętla główna: między 2:00 a 3:00 co 5 minut ===
print("🟢 Bot działa. Sprawdza tylko między 02:00 a 03:00...")

while True:
    now = datetime.now()
    if now.hour == 2:
        check_news()
        time.sleep(300)  # 5 minut
    else:
        time.sleep(60)
