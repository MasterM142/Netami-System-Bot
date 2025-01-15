import discord
from discord import app_commands
from discord.ext import commands

class TempChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}
        self.setup_channels = {}

    @commands.command(name="tempvoice")
    @commands.has_permissions(administrator=True)
    async def tempvoice_prefix(self, ctx, category: discord.CategoryChannel = None):
        """Setup temporary voice channels (prefix command)"""
        if not category:
            embed = discord.Embed(
                title="Temporary Voice Setup Guide",
                description="Here's how to set up temporary voice channels:\n\n"
                           "1. Right-click on a category where you want temp channels\n"
                           "2. Copy the category ID (Developer Mode must be enabled)\n"
                           "3. Use `!tempvoice <category-id>`\n\n"
                           "Example: `!tempvoice 123456789`",
                color=discord.Color.blue()
            )
            return await ctx.send(embed=embed)

        join_channel = await ctx.guild.create_voice_channel(
            name="➕ Create Voice Channel",
            category=category
        )
        self.setup_channels[join_channel.id] = category.id
        
        embed = discord.Embed(
            title="✅ Temporary Voice Setup Complete!",
            description=f"System is ready!\n\n"
                       f"📌 Join {join_channel.mention} to create your own voice channel\n"
                       f"🔧 Channel creator gets full control\n"
                       f"🗑️ Channel auto-deletes when empty",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="tempvoice")
    @app_commands.describe(category="Select the category for temporary voice channels")
    @app_commands.checks.has_permissions(administrator=True)
    async def tempvoice_slash(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        """Setup temporary voice channels"""
        join_channel = await interaction.guild.create_voice_channel(
            name="➕ Create Voice Channel",
            category=category
        )
        self.setup_channels[join_channel.id] = category.id
        
        embed = discord.Embed(
            title="✅ Temporary Voice Setup Complete!",
            description=f"System is ready!\n\n"
                       f"📌 Join {join_channel.mention} to create your own voice channel\n"
                       f"🔧 Channel creator gets full control\n"
                       f"🗑️ Channel auto-deletes when empty",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Create temp channel when joining setup channel
        if after.channel and after.channel.id in self.setup_channels:
            category = self.bot.get_channel(self.setup_channels[after.channel.id])
            temp_channel = await member.guild.create_voice_channel(
                name=f"✏️ {member.name}'s Channel",
                category=category
            )
            await member.move_to(temp_channel)
            self.temp_channels[temp_channel.id] = member.id
            
            # Set permissions for channel creator
            await temp_channel.set_permissions(member, 
                manage_channels=True,
                manage_permissions=True,
                connect=True,
                speak=True
            )

            # Send private message to creator
            try:
                embed = discord.Embed(
                    title="🎮 Your Voice Channel",
                    description="Your temporary voice channel has been created!\n\n"
                               "You can:\n"
                               "✏️ Rename the channel\n"
                               "👥 Manage user permissions\n"
                               "🔒 Lock/unlock the channel\n\n"
                               "Channel will auto-delete when empty.",
                    color=discord.Color.blue()
                )
                await member.send(embed=embed)
            except:
                pass

        # Delete empty temp channels
        if before.channel and before.channel.id in self.temp_channels:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                del self.temp_channels[before.channel.id]

async def setup(bot):
    await bot.add_cog(TempChannel(bot))





