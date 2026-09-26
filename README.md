# Discord Moderation & Community Bot

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2)
![License](https://img.shields.io/badge/license-MIT-green)

A lightweight moderation and community bot for Discord, built with **discord.py 2** and slash commands.

## Features

| Feature | Description |
|---|---|
| 👋 Welcome messages | Embed with the new member's avatar and the member count |
| 🎭 Button role menu | `/rolemenu` posts buttons that members click to add/remove roles. Buttons keep working after restarts |
| 🔇 Moderation | `/timeout`, `/kick`, `/ban`, `/clear` with permission checks |
| 🚫 Word filter | Messages containing banned words are deleted automatically |
| 📝 Mod log | Every moderation action is logged to a dedicated channel |
| ℹ️ Utility | `/userinfo`, `/ping` |

## Commands

| Command | Permission | Example |
|---|---|---|
| `/ping` | — | `/ping` |
| `/userinfo [member]` | — | `/userinfo @alex` |
| `/clear <amount>` | Manage Messages | `/clear 20` |
| `/timeout <member> <minutes> [reason]` | Moderate Members | `/timeout @alex 10 spam` |
| `/kick <member> [reason]` | Kick Members | `/kick @alex` |
| `/ban <member> [reason]` | Ban Members | `/ban @alex raiding` |
| `/rolemenu <roles>` | Manage Roles | `/rolemenu Gamer, Music, Art` |

## Setup

1. Create an application at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Under **Bot**, copy the token and enable **Server Members Intent** and **Message Content Intent**.
3. Under **OAuth2 → URL Generator**, select `bot` + `applications.commands` and invite the bot to your server.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and fill it in:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   WELCOME_CHANNEL_ID=123456789012345678
   LOG_CHANNEL_ID=123456789012345678
   BAD_WORDS=word1,word2
   ```
6. Run the bot:
   ```bash
   python bot.py
   ```

> **Note:** The bot can only manage roles that are *below* its own role in Server Settings → Roles.

## License

MIT
