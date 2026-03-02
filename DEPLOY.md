# Deploy Mafia Props Bot to the Cloud

Deploy the bot to **Railway** or **Render** for 24/7 uptime. Your bot token stays in env vars (never committed).

---

## Option A: Railway (recommended)

1. **Create account** at [railway.app](https://railway.app) (GitHub login).

2. **New Project** → **Deploy from GitHub repo**
   - Connect GitHub and select your repo (or push this folder to a new repo first).
   - If you don't use GitHub: **Empty Project** → **Add Service** → **GitHub Repo** or **Deploy from local** with Railway CLI.

3. **Configure the service**
   - Railway will detect Python and use the `Procfile`.
   - Under **Settings** → **Deploy**, ensure the start command is `python bot.py` (or leave default if Procfile is used).

4. **Set environment variables**
   - Open your service → **Variables** tab.
   - Add:
   - `DISCORD_TOKEN` = your bot token
   - Optional: `WHITELIST_CHANNELS` = `123,456` (comma-separated channel IDs)
   - Optional: `WHITELIST_ROLES` = `789,012` (comma-separated role IDs)
   - Optional: `DM_ON_DELETE` = `true` to DM users when messages are deleted

5. **Deploy** – Railway builds and runs automatically. Check **Deployments** for logs.

---

## Option B: Render

1. **Create account** at [render.com](https://render.com).

2. **New** → **Background Worker**.

3. **Connect repo** – Link GitHub and select your repo (or push this folder first).

4. **Configure**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Plan:** Free (or paid for always-on)

5. **Environment**
   - Add variable: `DISCORD_TOKEN` = your bot token
   - Optional: `WHITELIST_CHANNELS`, `WHITELIST_ROLES`, `DM_ON_DELETE` (see above)

6. **Create Background Worker** – Render deploys and keeps it running.

---

## Before deploying

1. **Push to GitHub** (if using repo deploy):
   ```bash
   git init
   git add .
   git commit -m "Add Mafia Props Bot"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
   Ensure `config.py` is in `.gitignore` so your token is never pushed.

2. **Use env var for token** – Do not put your token in `config.py` or commit it. Use `DISCORD_TOKEN` in the host's dashboard only.

---

## Verify

Once deployed, the bot should appear online in your Discord server. Test with `!ping` (admin) or by posting a blocked link like `discord.gg/test`.
