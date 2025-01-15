import discord
from discord import app_commands
from discord.ext import commands
import datetime

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_counter = 0
        self.active_tickets = {}
        self.ticket_settings = {
            "support_role": None,
            "ticket_logs": None,
            "welcome_message": "Welcome to your ticket! Support will be with you shortly.",
            "max_tickets": 5
        }

    @app_commands.command(name="ticket", description="Create a support ticket")
    async def ticket(self, interaction: discord.Interaction, reason: str = None):
        if interaction.user.id in self.active_tickets:
            await interaction.response.send_message("You already have an active ticket!", ephemeral=True)
            return

        self.ticket_counter += 1
        ticket_channel = await interaction.guild.create_text_channel(
            f"ticket-{self.ticket_counter}",
            category=interaction.channel.category,
            overwrites={
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )

        embed = discord.Embed(
            title=f"Ticket #{self.ticket_counter}",
            description=self.ticket_settings["welcome_message"],
            color=discord.Color.blue()
        )
        embed.add_field(name="Created by", value=interaction.user.mention)
        if reason:
            embed.add_field(name="Reason", value=reason)
        
        message = await ticket_channel.send(embed=embed)
        await message.pin()
        
        self.active_tickets[interaction.user.id] = {
            "channel": ticket_channel,
            "created_at": datetime.datetime.now(),
            "reason": reason
        }
        
        await interaction.response.send_message(f"Ticket created! Check {ticket_channel.mention}", ephemeral=True)

    @app_commands.command(name="close", description="Close a ticket")
    async def close(self, interaction: discord.Interaction):
        if not isinstance(interaction.channel, discord.TextChannel) or not interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message("This command can only be used in ticket channels!", ephemeral=True)
            return

        embed = discord.Embed(
            title="Ticket Closed",
            description=f"Ticket closed by {interaction.user.mention}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        
        await interaction.channel.delete()
        
        for user_id, ticket in self.active_tickets.items():
            if ticket["channel"].id == interaction.channel.id:
                del self.active_tickets[user_id]
                break
    @app_commands.command(name="adduser", description="Add a user to the ticket")
    async def adduser(self, interaction: discord.Interaction, user: discord.Member):
        if not isinstance(interaction.channel, discord.TextChannel) or not interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message("This command can only be used in ticket channels!", ephemeral=True)
            return

        await interaction.channel.set_permissions(user, read_messages=True, send_messages=True)
        await interaction.response.send_message(f"{user.mention} has been added to the ticket.")

    @app_commands.command(name="removeuser", description="Remove a user from the ticket")
    async def removeuser(self, interaction: discord.Interaction, user: discord.Member):
        if not isinstance(interaction.channel, discord.TextChannel) or not interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message("This command can only be used in ticket channels!", ephemeral=True)
            return

        await interaction.channel.set_permissions(user, overwrite=None)
        await interaction.response.send_message(f"{user.mention} has been removed from the ticket.")

    @app_commands.command(name="ticketsetup", description="Configure ticket system settings")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticketsetup(self, interaction: discord.Interaction, setting: str, value: str):
        if setting == "support_role":
            role = interaction.guild.get_role(int(value))
            if not role:
                await interaction.response.send_message("Invalid role ID!", ephemeral=True)
                return
            self.ticket_settings["support_role"] = role.id
        elif setting == "logs":
            channel = interaction.guild.get_channel(int(value))
            if not channel:
                await interaction.response.send_message("Invalid channel ID!", ephemeral=True)
                return
            self.ticket_settings["ticket_logs"] = channel.id
        elif setting == "message":
            self.ticket_settings["welcome_message"] = value
        elif setting == "max_tickets":
            try:
                self.ticket_settings["max_tickets"] = int(value)
            except ValueError:
                await interaction.response.send_message("Invalid number!", ephemeral=True)
                return

        await interaction.response.send_message(f"Ticket setting `{setting}` updated!", ephemeral=True)

    @app_commands.command(name="transcript", description="Get ticket transcript")
    async def transcript(self, interaction: discord.Interaction):
        if not isinstance(interaction.channel, discord.TextChannel) or not interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message("This command can only be used in ticket channels!", ephemeral=True)
            return

        messages = []
        async for message in interaction.channel.history(limit=None, oldest_first=True):
            messages.append(f"{message.created_at} - {message.author}: {message.content}")

        transcript = "\n".join(messages)
        
        with open(f"ticket-{interaction.channel.name}.txt", "w", encoding="utf-8") as f:
            f.write(transcript)

        await interaction.response.send_message(file=discord.File(f"ticket-{interaction.channel.name}.txt"))

async def setup(bot):
    await bot.add_cog(Tickets(bot))
