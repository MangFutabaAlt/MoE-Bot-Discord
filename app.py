import sqlite3
import os
import discord
import offline_filter
from discord import app_commands

# Folder khusus untuk menyimpan database per user
DB_DIR = "database"

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def get_user_db_path(discord_id: str) -> str:
    return os.path.join(DB_DIR, f"{discord_id}.db")

def init_user_db(discord_id: str, username_dc: str, password: str):
    db_path = get_user_db_path(discord_id)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account (
            discord_id TEXT PRIMARY KEY,
            username_discord TEXT,
            password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            discord_id TEXT PRIMARY KEY,
            level INTEGER,
            exp INTEGER,
            kill INTEGER,
            death INTEGER,
            total_absen_bulan_ini INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decoder (
            discord_id TEXT PRIMARY KEY,
            epic_decoder INTEGER,
            premium_epic_decoder INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT
        )
    ''')

    cursor.execute("INSERT INTO account VALUES (?, ?, ?)", (discord_id, username_dc, password))
    cursor.execute("INSERT INTO stats VALUES (?, 1, 0, 0, 0, 1)", (discord_id,))
    cursor.execute("INSERT INTO decoder VALUES (?, 5, 1)", (discord_id,))
    cursor.executemany("INSERT INTO inventory (item_name) VALUES (?)", [("default_knife",), ("default_usp",)])

    conn.commit()
    conn.close()

def user_db_exists(discord_id: str) -> bool:
    return os.path.exists(get_user_db_path(discord_id))

def get_user_password(discord_id: str) -> str:
    db_path = get_user_db_path(discord_id)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM account WHERE discord_id = ?", (discord_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def update_user_password(discord_id: str, new_password: str):
    db_path = get_user_db_path(discord_id)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE account SET password = ? WHERE discord_id = ?", (new_password, discord_id))
    conn.commit()
    conn.close()


class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True  # WAJIB diaktifkan untuk melacak member baru/keluar
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print('MoE Bot successfully started!')
        
  # No OFFLINE talking 
    async def on_message(self, message: discord.Message): 
        await offline_filter.handle_message(message)

    # EVENT MEMBER JOIN & AUTO DM GUIDE
    async def on_member_join(self, member: discord.Member):
        target_channel_id = 1487095243273670809
        channel = self.get_channel(target_channel_id)

        if channel:
            welcome_text = (
                f"Welcome {member.mention} to **CSMoE Citrus**!\n"
                "Please read <#1507388801842942013> first for the download & play guide."
            )
            await channel.send(welcome_text)

        # DM Guide Teks Panjang
        dm_guide_text = (
            "## Welcome to the CSMoE Discord Server\n"
            "**CSMoE Guide**\n"
            "*This is a guide about csmoe so you don't get confused about where to start.*\n\n"
            "**A. Downloading Games (Android & PC)**\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1507604812802297877\n\n"
            "**B. Installing Patch (PC)**\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1507633146773114991\n"
            "**C. Installing Patch (Android)**\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1507640914481512558\n\n"
            "**D. Play Online (Android)**\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1518057805246894141\n"
            "**E. Play Online (PC)**\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1519957896534822945\n\n"
            "**F. Strange message when joining server**\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1519960411825242356\n\n"
            "## Additional Information\n"
            "*I. Minimum Specifications*\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1522781914178654419\n\n"
            "*II. Recommend Specifications*\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1531995957321924618\n\n"
            "**FAQ**\n"
            "> https://discord.com/channels/1391616110406668369/1507388801842942013/1543064376402116799"
        )

        try:
            await member.send(dm_guide_text)
        except discord.Forbidden:
            print(f"Gagal mengirim DM ke {member.name}, DM ditutup.")

    # EVENT MEMBER LEAVE
    async def on_member_remove(self, member: discord.Member):
        target_channel_id = 1487095243273670809
        channel = self.get_channel(target_channel_id)

        if channel:
            leave_text = f"**{member.name}** has left the server."
            await channel.send(leave_text)

bot = MyBot()

# 1. COMMAND REGISTER
@bot.tree.command(name="register", description="Register a CSMoE account using a Discord")
async def register(interaction: discord.Interaction, password: str):
    discord_id = str(interaction.user.id)
    username_dc = interaction.user.name
    
    if user_db_exists(discord_id):
        await interaction.response.send_message(
            "⚠️ **Registration Failed:** This Discord ID is already registered in the CSMoE system!", 
            ephemeral=True
        )
        return

    init_user_db(discord_id, username_dc, password)
    
    pesan_sukses = (
        "**Account created successfully**\n"
        f"Discord ID: `{discord_id}`\n"
        f"Password: `{password}`\n\n"
        "Keep your password secret and good luck, soldier! 🫡 (this is just a prototype, you can't use this account)"
    )
    
    await interaction.response.send_message(pesan_sukses, ephemeral=True)


# 2. RESET PASSWORD COMMAND
@bot.tree.command(name="resetpassword", description="Change your CSMoE account password")
async def reset_password(interaction: discord.Interaction, password_lama: str, password_baru: str):
    discord_id = str(interaction.user.id)
    
    if not user_db_exists(discord_id):
        await interaction.response.send_message(
            "❌ **Error:** Account not found. Please register first using `/register`.", 
            ephemeral=True
        )
        return
    
    password_asli_di_db = get_user_password(discord_id)
    
    if password_asli_di_db != password_lama:
        await interaction.response.send_message(
            "🔒 **Error:** Incorrect current password!", 
            ephemeral=True
        )
        return

    if password_lama == password_baru:
        await interaction.response.send_message(
            "⚠️ **Error:** Your new password cannot be the same as your current password!", 
            ephemeral=True
        )
        return

    update_user_password(discord_id, password_baru)
    
    pesan_reset = (
        "**Password updated successfully**\n"
        f"Discord ID: `{discord_id}`\n"
        f"New Password: `{password_baru}`\n\n"
        "Your credentials have been updated. Good luck back on the field, soldier! 🫡"
    )
    
    await interaction.response.send_message(pesan_reset, ephemeral=True)

# Insert Bot Token
bot.run('token')
