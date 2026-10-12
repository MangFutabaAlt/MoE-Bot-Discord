import re
import discord

# User yang pesannya TIDAK akan dihapus
WHITELIST_IDS = {
    576101643687559211,
    1162541408528388206,
    421091319159455744,
}

# Kata kunci (case-insensitive, hanya kata utuh: "offline", "Offline", "OFFLINE")
KEYWORD_PATTERN = re.compile(r"\boffline\b", re.IGNORECASE)

REPLY_LINK = "https://discord.com/channels/1391616110406668369/1507388801842942013/1538407391685779456"


async def handle_message(message: discord.Message):
    # Abaikan bot, DM, dan user whitelist
    if message.author.bot or message.guild is None:
        return
    if message.author.id in WHITELIST_IDS:
        return
    if not KEYWORD_PATTERN.search(message.content):
        return

    try:
        await message.delete()
    except discord.Forbidden:
        print("Bot tidak punya izin Manage Messages di channel ini.")
    except discord.NotFound:
        pass

    await message.channel.send(
        f"{message.author.mention} Why are you talking about that? "
        f"Didn't you see {REPLY_LINK} ? (｡ŏ﹏ŏ)"
    )
    