import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime
from collections import defaultdict

# Hier die neuen Zeilen einfügen:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COGS_DIR = os.path.join(BASE_DIR, 'cogs')

# Dann geht es weiter mit:
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)
bot.points = {}
bot.temp_bans = {}
bot.custom_slowmodes = {}
bot.user_last_message = {}
bot.invite_tracker = defaultdict(dict)
bot.anti_nuke = defaultdict(lambda: {'actions': 0, 'last_reset': datetime.datetime.now()})
bot.raid_protection = {'enabled': False, 'account_age': 7, 'join_threshold': 10, 'join_window': 10}

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Netami's Discord Server"))
   
    guild = discord.Object(id=556552682865688603)
    
    for filename in os.listdir(COGS_DIR):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")


    # Force sync
    try:
        commands = await bot.tree.sync()
        print(f"Synced {len(commands)} commands!")
        print(f"Command names: {[cmd.name for cmd in commands]}")
    except Exception as e:
        print(f"Sync failed: {e}")

@bot.tree.command(name="help", description="Shows all available commands")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="NetamiTV - System Bot Commands", color=discord.Color.blue())
    
    mod_commands = """
    /ban - Ban a member
    /tempban - Temporarily ban a member
    /kick - Kick a member
    /mute - Mute a member
    /warn - Warn a member
    /timeout - Timeout a member
    /clear - Clear messages
    /purge - Delete all messages
    /lock - Lock a channel
    /unlock - Unlock a channel
    /slowmode - Set custom slowmode
    /role - Manage roles
    /lockdown - Lock entire server
    /unlockdown - Unlock entire server
    /massban - Mass ban suspicious users
    """
    
    protection_commands = """
    /antinuke - Configure anti-nuke
    /raidprotection - Configure raid protection
    /setinvitelog - Set invite tracking channel
    """
    
    utility_commands = """
    /serverinfo - Server information
    /userinfo - User information
    /getbadge - Active Developer Badge info
    /points - Show points
    /invitecheck - Check your invites privately
    /activatewindows - Windows activation guide
    /ping - Check bot latency
    /avatar - Get user avatar
    /about - Bot information
    """
    
    ticket_commands = """
    /ticket - Create a ticket
    /close - Close current ticket
    /adduser - Add user to ticket
    /removeuser - Remove user from ticket
    /ticketsetup - Configure ticket system
    """
    
    embed_commands = """
    /embedcreator - Create custom embeds
    /previewembed - Preview your embed
    /sendembed - Send your embed
    /saveembed - Save embed as preset
    /loadpreset - Load saved preset
    """
    
    counting_commands = """
    /points - Check your points
    /leaderboard - View top counters
    /resetpoints - Reset all points
    /setcount - Set current count
    """
    
    embed.add_field(name="Moderation Commands", value=mod_commands, inline=False)
    embed.add_field(name="Protection Commands", value=protection_commands, inline=False)
    embed.add_field(name="Utility Commands", value=utility_commands, inline=False)
    embed.add_field(name="Ticket Commands", value=ticket_commands, inline=False)
    embed.add_field(name="Embed Commands", value=embed_commands, inline=False)
    embed.add_field(name="Counting Commands", value=counting_commands, inline=False)
    embed.add_field(name="Counting System", value="Use +1 or -1 in counting channel", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command!", delete_after=5)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)

bot.run('')












