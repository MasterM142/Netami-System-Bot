import discord
from discord import app_commands
from discord.ext import commands

class EmbedBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_drafts = {}
        self.preset_embeds = {
            "welcome": {
                "title": "Welcome to our Server!",
                "description": "Please read our rules and enjoy your stay!",
                "color": discord.Color.green()
            },
            "rules": {
                "title": "Server Rules",
                "description": "1. Be respectful\n2. No spam\n3. No NSFW",
                "color": discord.Color.blue()
            }
        }

    @app_commands.command(name="embedcreator", description="Open the embed creator interface")
    async def embedcreator(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎨 Embed Creator",
            description="Use these commands to build your embed:\n\n"
                       "`/setembedtitle` - Set the title\n"
                       "`/setembeddesc` - Set the description\n"
                       "`/setembedcolor` - Set the color\n"
                       "`/addembedfield` - Add a field\n"
                       "`/setembedimage` - Set main image\n"
                       "`/setembedthumbnail` - Set thumbnail\n"
                       "`/setembedfooter` - Set footer\n"
                       "`/previewembed` - Preview current embed\n"
                       "`/sendembed` - Send the embed\n"
                       "`/saveembed` - Save as preset",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
        self.embed_drafts[interaction.user.id] = {}

    @app_commands.command(name="setembedtitle", description="Set embed title")
    async def setembedtitle(self, interaction: discord.Interaction, title: str):
        if interaction.user.id not in self.embed_drafts:
            self.embed_drafts[interaction.user.id] = {}
        
        self.embed_drafts[interaction.user.id]['title'] = title
        await interaction.response.send_message(f"Title set to: {title}", ephemeral=True)

    @app_commands.command(name="setembeddesc", description="Set embed description")
    async def setembeddesc(self, interaction: discord.Interaction, description: str):
        if interaction.user.id not in self.embed_drafts:
            self.embed_drafts[interaction.user.id] = {}
        
        self.embed_drafts[interaction.user.id]['description'] = description
        await interaction.response.send_message("Description set!", ephemeral=True)

    @app_commands.command(name="setembedcolor", description="Set embed color")
    async def setembedcolor(self, interaction: discord.Interaction, color: str):
        if interaction.user.id not in self.embed_drafts:
            self.embed_drafts[interaction.user.id] = {}
        
        try:
            color_value = int(color.strip('#'), 16) if color.startswith('#') else int(color)
            self.embed_drafts[interaction.user.id]['color'] = color_value
            await interaction.response.send_message(f"Color set to: {color}", ephemeral=True)
        except:
            await interaction.response.send_message("Invalid color format! Use hex (#FF0000) or decimal.", ephemeral=True)

    @app_commands.command(name="addembedfield", description="Add field to embed")
    async def addembedfield(self, interaction: discord.Interaction, name: str, value: str, inline: bool = True):
        if interaction.user.id not in self.embed_drafts:
            self.embed_drafts[interaction.user.id] = {}
        
        if 'fields' not in self.embed_drafts[interaction.user.id]:
            self.embed_drafts[interaction.user.id]['fields'] = []
        
        self.embed_drafts[interaction.user.id]['fields'].append({
            'name': name,
            'value': value,
            'inline': inline
        })
        await interaction.response.send_message(f"Field added: {name}", ephemeral=True)

    @app_commands.command(name="setembedimage", description="Set embed main image")
    async def setembedimage(self, interaction: discord.Interaction, url: str):
        if interaction.user.id not in self.embed_drafts:
            self.embed_drafts[interaction.user.id] = {}
        
        self.embed_drafts[interaction.user.id]['image'] = url
        await interaction.response.send_message("Image set!", ephemeral=True)

    @app_commands.command(name="setembedthumbnail", description="Set embed thumbnail")
    async def setembedthumbnail(self, interaction: discord.Interaction, url: str):
        if interaction.user.id not in self.embed_drafts:
            self.embed_drafts[interaction.user.id] = {}
        
        self.embed_drafts[interaction.user.id]['thumbnail'] = url
        await interaction.response.send_message("Thumbnail set!", ephemeral=True)

    @app_commands.command(name="setembedfooter", description="Set embed footer")
    async def setembedfooter(self, interaction: discord.Interaction, text: str, icon_url: str = None):
        if interaction.user.id not in self.embed_drafts:
            self.embed_drafts[interaction.user.id] = {}
        
        self.embed_drafts[interaction.user.id]['footer'] = {'text': text, 'icon_url': icon_url}
        await interaction.response.send_message("Footer set!", ephemeral=True)

    @app_commands.command(name="previewembed", description="Preview your embed")
    async def previewembed(self, interaction: discord.Interaction):
        if interaction.user.id not in self.embed_drafts:
            await interaction.response.send_message("No embed in progress! Use /embedcreator to start.", ephemeral=True)
            return
        
        draft = self.embed_drafts[interaction.user.id]
        embed = discord.Embed(
            title=draft.get('title', "No title set"),
            description=draft.get('description', "No description set"),
            color=draft.get('color', discord.Color.blue())
        )
        
        if 'fields' in draft:
            for field in draft['fields']:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        
        if 'image' in draft:
            embed.set_image(url=draft['image'])
        
        if 'thumbnail' in draft:
            embed.set_thumbnail(url=draft['thumbnail'])
        
        if 'footer' in draft:
            embed.set_footer(text=draft['footer']['text'], icon_url=draft['footer'].get('icon_url'))
        
        await interaction.response.send_message("Preview of your embed:", embed=embed)

    @app_commands.command(name="sendembed", description="Send your created embed")
    async def sendembed(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        if interaction.user.id not in self.embed_drafts:
            await interaction.response.send_message("No embed in progress!", ephemeral=True)
            return
        
        draft = self.embed_drafts[interaction.user.id]
        embed = discord.Embed(
            title=draft.get('title', "No title set"),
            description=draft.get('description', "No description set"),
            color=draft.get('color', discord.Color.blue())
        )
        
        if 'fields' in draft:
            for field in draft['fields']:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        
        if 'image' in draft:
            embed.set_image(url=draft['image'])
        
        if 'thumbnail' in draft:
            embed.set_thumbnail(url=draft['thumbnail'])
        
        if 'footer' in draft:
            embed.set_footer(text=draft['footer']['text'], icon_url=draft['footer'].get('icon_url'))
        
        target_channel = channel or interaction.channel
        await target_channel.send(embed=embed)
        await interaction.response.send_message("Embed sent!", ephemeral=True)
        del self.embed_drafts[interaction.user.id]

    @app_commands.command(name="saveembed", description="Save current embed as preset")
    async def saveembed(self, interaction: discord.Interaction, name: str):
        if interaction.user.id not in self.embed_drafts:
            await interaction.response.send_message("No embed in progress!", ephemeral=True)
            return
        
        self.preset_embeds[name] = self.embed_drafts[interaction.user.id].copy()
        await interaction.response.send_message(f"Saved preset '{name}'!", ephemeral=True)

    @app_commands.command(name="loadpreset", description="Load a saved preset")
    async def loadpreset(self, interaction: discord.Interaction, name: str):
        if name not in self.preset_embeds:
            await interaction.response.send_message("Preset not found!", ephemeral=True)
            return
        
        self.embed_drafts[interaction.user.id] = self.preset_embeds[name].copy()
        await interaction.response.send_message(f"Loaded preset '{name}'!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(EmbedBuilder(bot))
