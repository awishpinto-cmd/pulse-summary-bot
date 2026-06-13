import datetime
import os
import requests
from bs4 import BeautifulSoup
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def scrape_top_headlines():
    url = "https://news.ycombinator.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        print("Fetching top stories from Hacker News...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        story_spans = soup.find_all("span", class_="titleline")
        
        articles = []
        for span in story_spans[:5]:
            anchor_tag = span.find("a")
            if anchor_tag:
                title = anchor_tag.text.strip()
                link = anchor_tag.get("href")
                if link.startswith("item?id="):
                    link = f"https://news.ycombinator.com/{link}"
                articles.append({"title": title, "url": link})
                
        return articles
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

def build_html_email_content(articles):
    current_time = datetime.datetime.now().strftime("%I:%M %p on %A, %b %d, %Y")
    
    html = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
        <h2 style="color: #ff6600; border-bottom: 2px solid #ff6600; padding-bottom: 8px; margin-top: 0;">📰 Tech News Briefing</h2>
        <p style="font-size: 0.9em; color: #666; font-style: italic;">Compiled at {current_time}</p>
        <p>Good morning! Here are today's top technical headlines:</p>
        <hr style="border: 0; border-top: 1px solid #eeeeee; margin: 20px 0;">
        <ul style="list-style-type: none; padding-left: 0;">
    """
    
    if not articles:
        html += '<li style="color: #999;">Could not fetch headlines this morning.</li>'
    else:
        for index, item in enumerate(articles, start=1):
            html += f"""
            <li style="margin-bottom: 20px; padding: 10px; background-color: #fafafa; border-left: 4px solid #ff6600; border-radius: 0 4px 4px 0;">
                <strong style="font-size: 1.1em; color: #111;">{index}. {item['title']}</strong><br>
                <a href="{item['url']}" target="_blank" style="color: #0066cc; text-decoration: none; font-size: 0.9em;">Read Article →</a>
            </li>
            """
            
    html += """
        </ul>
        <hr style="border: 0; border-top: 1px solid #eeeeee; margin: 20px 0;">
        <p style="font-size: 0.8em; color: #999; text-align: center; margin-bottom: 0;">Automated pipeline active via GitHub Actions.</p>
    </body>
    </html>
    """
    return html

def send_email(html_content):
    # FALLBACK SETUP: Get credentials from Environment Variables (for GitHub Actions)
    # If running locally, it defaults to your hardcoded strings
    sender_email = os.environ.get("SENDER_EMAIL", "YOUR_GMAIL_ADDRESS@gmail.com")
    receiver_email = os.environ.get("RECEIVER_EMAIL", "YOUR_GMAIL_ADDRESS@gmail.com")
    app_password = os.environ.get("EMAIL_APP_PASSWORD", "YOUR_16_CHARACTER_APP_PASSWORD")

    # If you haven't replaced the placeholder strings locally yet, prevent execution errors
    if "YOUR_" in app_password or "YOUR_" in sender_email:
        print("\nSkipping email dispatch: Please replace email configuration placeholders with your actual credentials.")
        return

    print("Initializing secure secure connection to SMTP server...")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🎯 Morning Tech Briefing - {datetime.date.today().strftime('%b %d')}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Attach the styled HTML content
    msg.attach(MIMEText(html_content, "html"))

    try:
        # Establish connection to Gmail secure SMTP relay server
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.close()
        print("Email dispatched successfully! Check your inbox.")
    except Exception as e:
        print(f"SMTP Transmission Failed: {e}")

def run():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    headlines = scrape_top_headlines()
    email_markup = build_html_email_content(headlines)
    
    # Send the live briefing straight to your mail server
    send_email(email_markup)

if __name__ == "__main__":
    run()