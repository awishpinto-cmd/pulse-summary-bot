# Pulse: Automated Daily Summary Bot

Pulse is an automated daily summary bot that fetches the current weather forecast for Pavaratty (via `wttr.in`) and an inspirational Quote of the Day (via `zenquotes.io`). It aggregates these details, formats them into a clean daily summary file, and saves it.

The project is configured to run automatically every morning using **GitHub Actions**.

## Project Structure

```text
pulse-summary-bot/
 ├── .github/
 │    └── workflows/
 │         └── daily_summary.yml   # The GitHub Actions workflow file
 ├── bot.py                       # The Python automation script
 ├── requirements.txt             # Python dependencies
 └── README.md                    # Project documentation
```

## Features

- **Modular Design**: Structured into dedicated functions: `get_weather()`, `get_quote()`, `build_summary()`, and `run()`.
- **Resilience**: Features exception-handled API callers with sensible fallback values (`"Weather unavailable today"` / `'"Keep moving forward." — Anonymous'`) so the automation pipeline never crashes if third-party APIs go down.
- **GitHub Actions Automation**: Triggers daily at **06:00 AM IST** (00:30 AM UTC) and saves the generated `daily_summary.txt` as a downloadable artifact.

---

## Local Setup & Run

### 1. Install Dependencies
Make sure you have Python 3 installed. Install the required `requests` library:
```bash
pip install -r requirements.txt
```

### 2. Run the Script
Execute the script locally to generate the summary:
```bash
python bot.py
```
This will print the summary output to the console and write it to `daily_summary.txt` in the root folder.

---

## GitHub Deployment & Automation

To run the bot automatically in your own repository:

### 1. Initialize Git and Push to GitHub
1. Create a new repository on GitHub.
2. Initialize and push this project folder to your repository:
   ```bash
   git init
   git add .
   git commit -m "feat: setup pulse autonomous bot"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

### 2. Manually Triggering the Bot
1. Navigate to your repository on GitHub.
2. Click on the **Actions** tab.
3. Select **Run Pulse Daily** from the list of workflows on the left sidebar.
4. Click the **Run workflow** dropdown, and then click the green **Run workflow** button.

### 3. Retrieve the Summary File
Once the action completes successfully:
1. Click on the completed run in the Actions log.
2. Scroll down to the **Artifacts** section at the bottom of the page.
3. Click on **daily-summary-artifact** to download the generated `daily_summary.txt`.
