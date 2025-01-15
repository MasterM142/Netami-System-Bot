import discord
from discord import app_commands
from discord.ext import commands
import datetime

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Get server information")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        total_members = guild.member_count
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])
        
        embed = discord.Embed(title=f"{guild.name} Information", color=discord.Color.blue())
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="General", value=f"Owner: {guild.owner}\nCreated: {guild.created_at.strftime('%Y-%m-%d')}\nServer ID: {guild.id}", inline=False)
        embed.add_field(name="Members", value=f"Total: {total_members}\nHumans: {humans}\nBots: {bots}", inline=True)
        embed.add_field(name="Channels", value=f"Text: {text_channels}\nVoice: {voice_channels}", inline=True)
        embed.add_field(name="Boost Level", value=f"Level {guild.premium_tier}", inline=True)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Get user information")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        roles = [role.mention for role in member.roles[1:]]
        
        embed = discord.Embed(title="User Information", color=member.color)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Roles", value=" ".join(roles) if roles else "None", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="activatewindows", description="Get Windows activation instructions")
    async def activatewindows(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Windows Activation Guide",
            description="On Windows 8.1/10/11, right-click on the Windows start menu and select PowerShell or Terminal (Not CMD).\n\nCopy-paste the below code and press enter:\n```irm https://massgrave.dev/get | iex```\n\nYou will see the activation options, and follow onscreen instructions.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {round(self.bot.latency * 1000)}ms",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Get user's avatar")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.blue())
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inviteinfo", description="Check your invites")
    async def inviteinfo(self, interaction: discord.Interaction):
        total_invites = 0
        invites = await interaction.guild.invites()
        user_invites = [invite for invite in invites if invite.inviter == interaction.user]
        
        embed = discord.Embed(title="Your Invite Statistics", color=discord.Color.blue())
        
        for invite in user_invites:
            embed.add_field(
                name=f"Invite Code: {invite.code}",
                value=f"Uses: {invite.uses}\nChannel: {invite.channel.mention}",
                inline=False
            )
            total_invites += invite.uses
        
        embed.set_footer(text=f"Total Invites: {total_invites}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="membercount", description="Show server member statistics")
    async def membercount(self, interaction: discord.Interaction):
        guild = interaction.guild
        total = guild.member_count
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])
        
        embed = discord.Embed(title="Member Statistics", color=discord.Color.blue())
        embed.add_field(name="Total Members", value=str(total))
        embed.add_field(name="Humans", value=str(humans))
        embed.add_field(name="Bots", value=str(bots))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roleinfo", description="Get information about a role")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(title=f"Role Information: {role.name}", color=role.color)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Created", value=role.created_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Members", value=len(role.members))
        embed.add_field(name="Mentionable", value=role.mentionable)
        embed.add_field(name="Displayed Separately", value=role.hoist)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="channelinfo", description="Get information about a channel")
    async def channelinfo(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        embed = discord.Embed(title=f"Channel Information: {channel.name}", color=discord.Color.blue())
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Created", value=channel.created_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Category", value=channel.category.name if channel.category else "None")
        embed.add_field(name="Topic", value=channel.topic or "No topic set")
        embed.add_field(name="Slowmode", value=f"{channel.slowmode_delay}s")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="getbadge", description="Get Active Developer Badge info")
    async def getbadge(self, interaction: discord.Interaction):
        embed = discord.Embed(title="How to get Active Developer Badge", color=discord.Color.blue())
        embed.add_field(name="Steps", value=
            "1. Create a Discord Application and Bot\n"
            "2. Enable Developer Mode\n"
            "3. Create a slash command\n"
            "4. Run your bot and use the command\n"
            "5. Wait 24 hours\n"
            "6. Visit: discord.com/developers/active-developer\n"
            "7. Claim your badge!", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="about", description="About the bot")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="About Netami - System Bot",
            description="Im the SystemBot from masterM who manage his content and all important features",
            color=discord.Color.blue()
        )
        embed.add_field(name="Developer", value="MasterM142", inline=True)
        embed.add_field(name="Version", value="2.1.7", inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Commands", value="Use /help to see all commands", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
