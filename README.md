# MoE-Bot-Discord

MoE-Bot-Discord is a Discord bot built with discord.py designed to manage the CSMoE Citrus gaming community. It features a per-user database registration system, automated guide distribution via direct messages for new members, and automated join/leave notifications in server channels.

---

## Key Features

- Per-User Account System (SQLite3):
  - Creates an isolated SQLite database (`database/<discord_id>.db`) for each user.
  - Slash command (`/register`) to set up new accounts (username & password) with starting inventory.
  - Slash command (`/resetpassword`) to safely update account passwords.
- Welcome & Farewell Events:
  - Greets new members in public channels.
  - Automatically sends a detailed guide (downloads, patches, online setup, hardware specs, FAQ) via DM to new members.
  - Posts notification messages whenever a member leaves the server.
- Offline Filter Integration:
  - Automatically filters incoming messages using the custom `offline_filter` module.

---

## Prerequisites & Tech Stack

- Python 3.10+
- Python Libraries:
  - discord.py
  - sqlite3 (Built-in)

---

## Installation & Setup

1. Clone the Repository
   git clone [https://github.com/MangFutabaAlt/MoE-Bot-Discord.git](https://github.com/MangFutabaAlt/MoE-Bot-Discord.git)
   cd MoE-Bot-Discord

2. Install Dependencies
   pip install discord.py

3. Configure Bot Token & Intents
   - Open app.py.
   - Update the bottom line with your Discord bot token:
     bot.run('YOUR_BOT_TOKEN_HERE')
   - Ensure both Server Members Intent and Message Content Intent are enabled in the Discord Developer Portal.

4. Run the Bot
   python app.py

---

## Slash Commands

| Command | Description | Parameters |
| :--- | :--- | :--- |
| `/register` | Registers a new CSMoE account | `password`: Account password |
| `/resetpassword` | Resets your CSMoE account password | `password_lama`, `password_baru` |

---

## Security Note

Important: Never commit or push your actual Discord bot token publicly to GitHub. Use Environment Variables (`.env`) or make sure to sanitize your credentials before running `git push`.
