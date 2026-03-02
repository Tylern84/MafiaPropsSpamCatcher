"""
Mafia Props Bot - Anti-Spam Discord Bot
Blocks Discord invite links and Telegram links to reduce spam in your community.
"""

import os
import re
import discord
from discord.ext import commands

# Load config: env vars (cloud) take precedence over config.py (local)
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
WHITELIST_CHANNELS = []
WHITELIST_ROLES = []
DM_ON_DELETE = False

if not DISCORD_TOKEN:
    try:
        from config import (
            DISCORD_TOKEN as _TOKEN,
            WHITELIST_CHANNELS as _CH,
            WHITELIST_ROLES as _R,
            DM_ON_DELETE as _DM,
        )
        DISCORD_TOKEN = _TOKEN
        WHITELIST_CHANNELS = _CH
        WHITELIST_ROLES = _R
        DM_ON_DELETE = _DM
    except ImportError:
        pass

# Optional: load whitelists from env (comma-separated IDs)
if os.environ.get("WHITELIST_CHANNELS"):
    WHITELIST_CHANNELS = [int(x) for x in os.environ["WHITELIST_CHANNELS"].split(",") if x.strip()]
if os.environ.get("WHITELIST_ROLES"):
    WHITELIST_ROLES = [int(x) for x in os.environ["WHITELIST_ROLES"].split(",") if x.strip()]
if os.environ.get("DM_ON_DELETE", "").lower() in ("1", "true", "yes"):
    DM_ON_DELETE = True

if not DISCORD_TOKEN:
    print("ERROR: Set DISCORD_TOKEN (env var or config.py)")
    exit(1)

# Patterns for spam links
DISCORD_INVITE_PATTERNS = [
    r"discord\.gg/[\w-]+",
    r"discord\.com/invite/[\w-]+",
    r"discordapp\.com/invite/[\w-]+",
]

TELEGRAM_PATTERNS = [
    r"t\.me/[\w]+",
    r"telegram\.me/[\w]+",
    r"telegram\.dog/[\w]+",
]

ALL_PATTERNS = [re.compile(p, re.IGNORECASE) for p in DISCORD_INVITE_PATTERNS + TELEGRAM_PATTERNS]


def contains_spam_links(text: str) -> bool:
    """Check if the message contains any blocked links."""
    if not text:
        return False
    for pattern in ALL_PATTERNS:
        if pattern.search(text):
            return True
    return False


def is_whitelisted(message: discord.Message) -> bool:
    """Check if the message author or channel is whitelisted."""
    if message.channel.id in WHITELIST_CHANNELS:
        return True
    if isinstance(message.author, discord.Member):
        for role in message.author.roles:
            if role.id in WHITELIST_ROLES:
                return True
    return False


# Bot setup
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True  # Required for role whitelist; enable Server Members Intent in Developer Portal

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Connected to {len(bot.guilds)} guild(s)")
    print("Anti-spam filter is active. Blocking Discord invites & Telegram links.")
    print("-" * 50)


@bot.event
async def on_message(message: discord.Message):
    # Ignore bot messages
    if message.author.bot:
        await bot.process_commands(message)
        return

    # Check for spam links
    if contains_spam_links(message.content):
        if is_whitelisted(message):
            await bot.process_commands(message)
            return

        try:
            await message.delete()
            print(f"Deleted spam from {message.author} in #{message.channel}: {message.content[:80]}...")

            if DM_ON_DELETE:
                try:
                    await message.author.send(
                        f"Your message in **{message.guild.name}** was removed because it contained "
                        "a Discord or Telegram link. Sharing invite links is not allowed."
                    )
                except discord.Forbidden:
                    pass  # User has DMs disabled
        except discord.Forbidden:
            print(f"Could not delete message: missing permissions in #{message.channel}")
        except discord.NotFound:
            pass  # Message already deleted

    await bot.process_commands(message)


@bot.command(name="ping")
@commands.has_permissions(administrator=True)
async def ping(ctx):
    """Check if the bot is responsive (admin only)."""
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")


def main():
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
