import discord
from discord import app_commands
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_bans = {}

    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("You can't ban this user!", ephemeral=True)
            return
        await member.ban(reason=reason)
        embed = discord.Embed(title="Member Banned", description=f"{member} was banned by {interaction.user}\nReason: {reason}", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("You can't kick this user!", ephemeral=True)
            return
        await member.kick(reason=reason)
        embed = discord.Embed(title="Member Kicked", description=f"{member} was kicked by {interaction.user}\nReason: {reason}", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mute", description="Mute a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.timeout(duration=None, reason=reason)
        embed = discord.Embed(title="Member Muted", description=f"{member} was muted by {interaction.user}\nReason: {reason}", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unmute", description="Unmute a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(duration=0)
        embed = discord.Embed(title="Member Unmuted", description=f"{member} was unmuted by {interaction.user}", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="tempban", description="Temporarily ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def tempban(self, interaction: discord.Interaction, member: discord.Member, hours: int, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("You can't ban this user!", ephemeral=True)
            return
        await member.ban(reason=f"Tempban: {reason}")
        self.temp_bans[member.id] = {
            'unban_time': datetime.datetime.now() + datetime.timedelta(hours=hours),
            'guild_id': interaction.guild.id
        }
        embed = discord.Embed(title="Member Temporarily Banned", description=f"{member} was banned for {hours} hours\nReason: {reason}", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        embed = discord.Embed(title="Member Warned", description=f"{member} was warned by {interaction.user}\nReason: {reason}", color=discord.Color.yellow())
        await interaction.response.send_message(embed=embed)
        try:
            await member.send(f"You were warned in {interaction.guild.name} for: {reason}")
        except:
            pass

    @app_commands.command(name="clear", description="Clear messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(title="Messages Cleared", description=f"{amount} messages were cleared by {interaction.user}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, delete_after=5)

    @app_commands.command(name="lock", description="Lock a channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        embed = discord.Embed(title="Channel Locked", description=f"Channel locked by {interaction.user}", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unlock", description="Unlock a channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        embed = discord.Embed(title="Channel Unlocked", description=f"Channel unlocked by {interaction.user}", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="slowmode", description="Set custom slowmode duration")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        await interaction.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(title="Slowmode Set", description=f"Slowmode set to {seconds} seconds", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
