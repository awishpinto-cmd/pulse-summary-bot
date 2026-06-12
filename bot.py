import datetime
import requests
import sys

def get_weather():
    try:
        # Fetch plain-text weather overview
        response = requests.get("https://wttr.in/Pavaratty?format=3", timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception:
        # Fallback value if the API is down
        return "Weather unavailable today"

def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/today", timeout=10)
        response.raise_for_status()
        data = response.json()
        # Extract quote and author from JSON list
        return f'"{data[0]["q"]}" — {data[0]["a"]}'
    except Exception:
        return '"Keep moving forward." — Anonymous'

def build_summary(weather, quote):
    today = datetime.date.today().strftime("%A, %b %d, %Y")
    
    # Use triple quotes for clean multi-line formatting
    summary = f"""
=========================================
DAILY PULSE SUMMARY — {today}
=========================================

WEATHER:
{weather}

TODAY'S QUOTE:
{quote}

=========================================
"""
    return summary

def run():
    # Reconfigure stdout to use UTF-8, preventing UnicodeEncodeError on Windows console
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("Pulse is active...")
    weather = get_weather()
    quote = get_quote()
    
    summary_text = build_summary(weather, quote)
    print(summary_text)
    
    # Save the output to a text file using UTF-8 encoding
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)
        
    print("Done! daily_summary.txt written successfully.")

if __name__ == "__main__":
    run()
