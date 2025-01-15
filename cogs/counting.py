import discord
from discord.ext import commands
from discord import app_commands
import json
import datetime

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.points = {}
        self.COUNTING_CHANNEL_ID = 1321136302141210634
        self.last_number = 0
        self.last_counter = None
        try:
            with open('counting_data.json', 'r') as f:
                data = json.load(f)
                self.points = data.get('points', {})
                self.last_number = data.get('last_number', 0)
        except:
            pass

    def save_data(self):
        with open('counting_data.json', 'w') as f:
            json.dump({
                'points': self.points,
                'last_number': self.last_number
            }, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.id != self.COUNTING_CHANNEL_ID:
            return

        # Handle counting messages
        if message.content in ["+1", "-1"]:
            if message.content == "+1":
                if str(message.author.id) not in self.points:
                    self.points[str(message.author.id)] = 0

                self.last_number += 1
                self.points[str(message.author.id)] += 1
                self.last_counter = message.author.id
                await message.add_reaction("✅")
                self.save_data()

            elif message.content == "-1":
                if str(message.author.id) not in self.points:
                    self.points[str(message.author.id)] = 0
                
                if message.author.id == self.last_counter:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} you can't count twice in a row!", delete_after=5)
                    return

                if self.last_number <= 0:
                    await message.delete()
                    await message.channel.send("Can't go below 0!", delete_after=5)
                    return

                self.last_number -= 1
                self.points[str(message.author.id)] -= 1
                self.last_counter = message.author.id
                await message.add_reaction("✅")
                self.save_data()

    @app_commands.command(name="points", description="Check counting points")
    async def points(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        points = self.points.get(str(member.id), 0)
        
        embed = discord.Embed(
            title="Counting Points",
            description=f"{member.mention} has {points} points",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="Show counting leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        sorted_points = sorted(self.points.items(), key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(
            title="Counting Leaderboard",
            color=discord.Color.gold()
        )
        
        for i, (user_id, points) in enumerate(sorted_points[:10], 1):
            user = interaction.guild.get_member(int(user_id))
            if user:
                embed.add_field(
                    name=f"#{i} {user.name}",
                    value=f"Points: {points}",
                    inline=False
                )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="resetpoints", description="Reset all counting points")
    @app_commands.checks.has_permissions(administrator=True)
    async def resetpoints(self, interaction: discord.Interaction):
        self.points.clear()
        self.last_number = 0
        self.last_counter = None
        self.save_data()
        
        embed = discord.Embed(
            title="Points Reset",
            description="All counting points have been reset!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setcount", description="Set the current count number")
    @app_commands.checks.has_permissions(administrator=True)
    async def setcount(self, interaction: discord.Interaction, number: int):
        self.last_number = number
        self.save_data()
        
        embed = discord.Embed(
            title="Count Updated",
            description=f"The current count has been set to {number}",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Counting(bot))


