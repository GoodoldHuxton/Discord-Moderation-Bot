# Discord Moderation Bot

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2)
![License](https://img.shields.io/badge/license-MIT-green)

A customizable Discord moderation and community management bot built with Python, featuring slash commands, role menus, welcome messages and moderation logs.

Built for communities that want to automate repetitive moderation and management tasks.

<!-- Screenshot: add assets/screenshot.png (e.g. the /rolemenu buttons or a welcome embed) and uncomment the line below -->
<!-- ![Discord Moderation Bot screenshot](assets/screenshot.png) -->

## Features

| Feature | Description |
|---|---|
| 👋 Welcome messages | Embed with the new member's avatar and the member count |
| 🎭 Button role menu | `/rolemenu` posts buttons that members click to add/remove roles. Buttons keep working after restarts |
| 🔇 Moderation | `/timeout`, `/kick`, `/ban`, `/clear` with permission checks |
| 🚫 Word filter | Messages containing banned words are deleted automatically |
| 📝 Mod log | Every moderation action is logged to a dedicated channel |
| ℹ️ Utility | `/userinfo`, `/ping` |

## Tech Stack

- Python 3.10+
- [discord.py](https://github.com/Rapptz/discord.py) 2.x (slash commands, persistent button views)
- python-dotenv (configuration via `.env`)

## Installation

1. Create an application at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Under **Bot**, copy the token and enable **Server Members Intent** and **Message Content Intent**.
3. Under **OAuth2 → URL Generator**, select `bot` + `applications.commands` and invite the bot to your server.
4. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/GoodoldHuxton/Discord-Moderation-Bot.git
   cd Discord-Moderation-Bot
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and fill it in:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   WELCOME_CHANNEL_ID=123456789012345678
   LOG_CHANNEL_ID=123456789012345678
   BAD_WORDS=word1,word2
   ```

> **Note:** The bot can only manage roles that are *below* its own role in Server Settings → Roles.

## Usage

Start the bot:

```bash
python bot.py
```

Then use the slash commands in your server:

| Command | Permission | Example |
|---|---|---|
| `/ping` | — | `/ping` |
| `/userinfo [member]` | — | `/userinfo @alex` |
| `/clear <amount>` | Manage Messages | `/clear 20` |
| `/timeout <member> <minutes> [reason]` | Moderate Members | `/timeout @alex 10 spam` |
| `/kick <member> [reason]` | Kick Members | `/kick @alex` |
| `/ban <member> [reason]` | Ban Members | `/ban @alex raiding` |
| `/rolemenu <roles>` | Manage Roles | `/rolemenu Gamer, Music, Art` |

## What problem it solves

Growing Discord servers spend a lot of moderator time on the same jobs: greeting new members, handing out roles, deleting spam and keeping track of who was warned or banned. This bot handles those jobs automatically and keeps a log of every action, so moderators can focus on the community instead of the busywork.

## Contact / Available for freelance work

Need a custom Discord bot for your server, with your own commands, tickets, levels or integrations? I build bots like this one to order.

- 📧 [skyiest15@gmail.com](mailto:skyiest15@gmail.com)
- 💼 [LinkedIn](https://www.linkedin.com/in/yi%C4%9Fit-alp-bayar-96630b268)

## License

MIT
