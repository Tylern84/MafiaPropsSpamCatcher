# Mafia Props Bot – Anti-Spam Discord Bot

A Discord bot that automatically removes messages containing **Discord invite links** and **Telegram links** to reduce spam in your server.

## Features

- Deletes messages with `discord.gg/`, `discord.com/invite/`, `discordapp.com/invite/`
- Deletes messages with `t.me/`, `telegram.me/`, `telegram.dog/`
- Optional whitelist for trusted channels or roles
- Optional DM to users when their message is removed

## Setup

### 1. Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** and give it a name (e.g. "Mafia Props Bot")
3. Go to **Bot** → **Add Bot**
4. Under **Privileged Gateway Intents**, enable:
   - **MESSAGE CONTENT INTENT**
   - **SERVER MEMBERS INTENT** (for role-based whitelist)
5. Copy your bot token

### 2. Invite the Bot to Your Server

1. Go to **OAuth2** → **URL Generator**
2. Scopes: select **bot**
3. Bot Permissions: select **Manage Messages**, **Send Messages**, **Read Message History**
4. Copy the generated URL and open it to add the bot to your server

### 3. Install and Run

```bash
pip install -r requirements.txt
cp config.example.py config.py
# Edit config.py and add your bot token
python bot.py
```

### 4. Configure `config.py`

```python
DISCORD_TOKEN = "your_bot_token_here"

# Optional: channels where links are allowed (e.g. announcements)
WHITELIST_CHANNELS = [123456789012345678]

# Optional: roles that can post links (e.g. moderators)
WHITELIST_ROLES = [987654321098765432]

# Optional: DM users when their message is deleted
DM_ON_DELETE = False
```

## Commands

- `!ping` – Check if the bot is online (admin only)

## Permissions

The bot needs:

- **Manage Messages** – to delete spam
- **Read Message History** – to read messages
- **Send Messages** – for commands
- **Message Content Intent** – in Developer Portal (Bot settings)

## Running 24/7

For a server that’s always on, run with:

```bash
./scripts/install-service.sh  # Mac: runs in background, auto-restart
```

Or use a process manager like **pm2** or **systemd**, or host it on a platform like **Railway**, **Render**, or **Replit**.

## Adding More Patterns

Edit `bot.py` and extend the pattern lists:

```python
# Example: block Instagram links
TELEGRAM_PATTERNS = [
    # ... existing ...
    r"instagram\.com/[\w.]+",
]
```
