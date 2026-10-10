
import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.presences = True


class EStatsBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()
        print("E Stats commands synced!")


bot = EStatsBot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("E Stats is online!")


def get_online_count(guild):
    return sum(
        1 for member in guild.members
        if member.status != discord.Status.offline
    )


@bot.tree.command(name="stats", description="View server statistics")
async def stats(interaction: discord.Interaction):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "Use this command inside a server.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🌌 Eclipse | E Stats",
        description="Server Statistics",
        color=discord.Color.purple()
    )
    embed.add_field(
        name="👥 Total Members",
        value=str(guild.member_count),
        inline=True
    )
    embed.add_field(
        name="🟢 Online Members",
        value=str(get_online_count(guild)),
        inline=True
    )
    embed.set_footer(text="E Stats • Eclipse Community")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="members", description="Show total members")
async def members(interaction: discord.Interaction):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "Use this command inside a server.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"👥 Total server members: **{guild.member_count}**"
    )


@bot.tree.command(name="online", description="Show online members")
async def online(interaction: discord.Interaction):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "Use this command inside a server.",
            ephemeral=True
        )
        return

    count = get_online_count(guild)
    await interaction.response.send_message(
        f"🟢 Non-offline members: **{count}**"
    )


@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(
        f"🏓 Pong! **{latency} ms**"
    )


@bot.tree.command(name="help", description="Show bot commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌌 E Stats | Commands",
        color=discord.Color.purple()
    )
    embed.add_field(name="/stats", value="Server statistics", inline=False)
    embed.add_field(name="/members", value="Total members", inline=False)
    embed.add_field(name="/online", value="Online members", inline=False)
    embed.add_field(name="/ping", value="Bot response time", inline=False)
    embed.add_field(name="/help", value="Show all commands", inline=False)

    await interaction.response.send_message(embed=embed)


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is missing!")

bot.run(TOKEN)
