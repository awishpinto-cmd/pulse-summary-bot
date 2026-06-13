import os
import requests
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def check_weather_and_alert():
    # Setup location configurations for Pavaratty/Thrissur, Kerala
    # Using open public geographic parameters (No API key required for standard lookups)
    city = "Thrissur"
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        print(f"Fetching current weather metrics for {city}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        weather_data = response.json()
        
        # Parse out current temperatures and conditions
        current_condition = weather_data['current_condition'][0]
        temp_c = float(current_condition['temp_C'])
        weather_desc = current_condition['weatherDesc'][0]['value'].lower()
        
        print(f"Current Metrics -> Temp: {temp_c}°C, Condition: {weather_desc}")
        
        # Core Threshold Logic Checks
        is_too_hot = temp_c > 35.0
        is_raining = "rain" in weather_desc or "shower" in weather_desc or "drizzle" in weather_desc
        
        if is_too_hot or is_raining:
            print("Weather threshold breached! Initializing email dispatch...")
            
            # Formulate the alert reasons
            reasons = []
            if is_too_hot: reasons.append(f"High Temperature Alert ({temp_c}°C)")
            if is_raining: reasons.append(f"Precipitation Warning ({weather_desc.title()})")
            
            subject = f"⚠️ Weather Alert: {', '.join(reasons)}"
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #cc0000; border-radius: 8px; max-width: 500px;">
                <h2 style="color: #cc0000; margin-top: 0;">⚠️ Weather Threshold Warning</h2>
                <p>The automated weather pipeline has detected critical weather conditions for <strong>{city}</strong>:</p>
                <ul>
                    <li><strong>Current Temperature:</strong> {temp_c}°C</li>
                    <li><strong>Current Condition:</strong> {weather_desc.title()}</li>
                </ul>
                <p style="color: #555; font-size: 0.9em;">Please plan your travel or field tasks accordingly.</p>
            </body>
            </html>
            """
            send_alert_email(subject, body)
        else:
            print("Weather is within standard thresholds. No alert email needed.")
            
    except Exception as e:
        print(f"Weather alert lookup failed: {e}")

def send_alert_email(subject, html_content):
    sender_email = os.environ.get("SENDER_EMAIL", "YOUR_GMAIL_ADDRESS@gmail.com")
    receiver_email = os.environ.get("RECEIVER_EMAIL", "YOUR_GMAIL_ADDRESS@gmail.com")
    app_password = os.environ.get("EMAIL_APP_PASSWORD", "YOUR_16_CHARACTER_APP_PASSWORD")

    if "YOUR_" in app_password:
        print("Skipping local dispatch: Placeholders active.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.close()
        print("Alert successfully sent to your inbox!")
    except Exception as e:
        print(f"SMTP Alert Transmission Failed: {e}")

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    check_weather_and_alert()