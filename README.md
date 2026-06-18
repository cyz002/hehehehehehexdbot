# 🎯 Countdown Bot — June 30 Reveal

A Telegram bot that shows a game-style progress bar counting down to June 30, then reveals an image on the big day.

## Commands
- `/start` — show the countdown progress bar
- `/days` — same as /start

## How the bar works
The bar fills from your `START_DATE` (default Jan 1 2025) to June 30. Each day the bar moves forward and the hype message escalates.

---

## 🚀 Deploy to Railway

### Step 1 — Create your Telegram bot
1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy the **token** it gives you (looks like `123456:ABCdef...`)

### Step 2 — Push to GitHub
```bash
git init
git add .
git commit -m "initial bot"
gh repo create countdown-bot --public --push
# or manually create a repo on github.com and push
```

### Step 3 — Deploy on Railway
1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **New Project → Deploy from GitHub repo**
3. Select your repo
4. Go to **Variables** tab and add:
   - `TELEGRAM_BOT_TOKEN` = your token from BotFather
5. Railway auto-detects Python and deploys. Done! ✅

---

## 🖼️ Swapping in the real image

In `bot.py`, find this line:
```python
PLACEHOLDER_IMAGE_URL = "https://placehold.co/..."
```

Replace it with either:
- A direct image URL: `"https://yoursite.com/reveal.jpg"`
- Or a Telegram `file_id` (send the image to your bot first, then grab the ID from the API)

Redeploy after changing it.

---

## 🔧 Customise

| Thing | Where |
|---|---|
| Start date for bar | `START_DATE` in bot.py |
| Target date | `TARGET_DATE` in bot.py |
| Hype messages | `build_countdown_message()` in bot.py |
| Reveal caption | The `caption=` in the `/start` handler |
