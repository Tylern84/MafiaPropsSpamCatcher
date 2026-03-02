#!/bin/bash
# Install the bot as a launchd service so it runs automatically and restarts on crash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PLIST_NAME="com.mafiaprops.spambot.plist"
PLIST_SRC="$PROJECT_DIR/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "Installing Mafia Props Bot service..."
cp "$PLIST_SRC" "$PLIST_DEST"
launchctl load "$PLIST_DEST"
echo "Done! Bot is now running and will start automatically on login."
echo ""
echo "Useful commands:"
echo "  Stop:   launchctl unload $PLIST_DEST"
echo "  Start:  launchctl load $PLIST_DEST"
echo "  Logs:   tail -f $PROJECT_DIR/bot.log"
