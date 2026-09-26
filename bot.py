import os
from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "0"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
BAD_WORDS = {w.strip().lower() for w in os.getenv("BAD_WORDS", "").split(",") if w.strip()}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def log(guild: discord.Guild, text: str):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(embed=discord.Embed(description=text, color=discord.Color.orange()))


# ---------- Button role menu ----------
class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role):
        super().__init__(label=role.name, style=discord.ButtonStyle.primary,
                         custom_id=f"role:{role.id}")

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.custom_id.split(":")[1])
        role = interaction.guild.get_role(role_id)
        if role is None:
            return await interaction.response.send_message("Role not found.", ephemeral=True)
        member = interaction.user
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"Removed **{role.name}**.", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"Added **{role.name}**.", ephemeral=True)


class RoleView(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)
        for role in roles:
            self.add_item(RoleButton(role))


# ---------- Events ----------
@bot.event
async def on_ready():
    # Keep existing role buttons working after a restart
    for guild in bot.guilds:
        roles = [r for r in guild.roles if not r.managed and not r.is_default()]
        bot.add_view(RoleView(roles[:25]))
    synced = await bot.tree.sync()
    print(f"Logged in as {bot.user}, synced {len(synced)} commands.")


@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Welcome!",
            description=f"{member.mention} just joined **{member.guild.name}**.\n"
                        f"We are now {member.guild.member_count} members.",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.guild:
        return
    if BAD_WORDS and any(w in message.content.lower() for w in BAD_WORDS):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, that word is not allowed.", delete_after=5)
        await log(message.guild, f"🚫 {message.author.mention} used a banned word: ||{message.content}||")
    await bot.process_commands(message)


# ---------- Slash commands ----------
@bot.tree.command(description="Show the bot's latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)} ms")


@bot.tree.command(description="Show information about a member")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=str(member), color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Account created", value=discord.utils.format_dt(member.created_at, "D"))
    embed.add_field(name="Joined server", value=discord.utils.format_dt(member.joined_at, "D"))
    embed.add_field(name="Roles", value=", ".join(r.mention for r in member.roles[1:]) or "None", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(description="Delete a number of recent messages")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🧹 Deleted {len(deleted)} messages.", ephemeral=True)
    await log(interaction.guild, f"🧹 {interaction.user.mention} deleted {len(deleted)} messages in {interaction.channel.mention}.")


@bot.tree.command(description="Time out a member for a number of minutes")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member,
                  minutes: app_commands.Range[int, 1, 40320], reason: str = "No reason given"):
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await interaction.response.send_message(f"🔇 {member.mention} timed out for {minutes} minutes. Reason: {reason}")
    await log(interaction.guild, f"🔇 {interaction.user.mention} → {member.mention} ({minutes} min). Reason: {reason}")


@bot.tree.command(description="Kick a member from the server")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason given"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 {member} was kicked. Reason: {reason}")
    await log(interaction.guild, f"👢 {interaction.user.mention} kicked {member}. Reason: {reason}")


@bot.tree.command(description="Ban a member from the server")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason given"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 {member} was banned. Reason: {reason}")
    await log(interaction.guild, f"🔨 {interaction.user.mention} banned {member}. Reason: {reason}")


@bot.tree.command(description="Create a button role menu (comma-separated role names)")
@app_commands.checks.has_permissions(manage_roles=True)
async def rolemenu(interaction: discord.Interaction, roles: str):
    names = [n.strip().lower() for n in roles.split(",")]
    found = [r for r in interaction.guild.roles if r.name.lower() in names]
    if not found:
        return await interaction.response.send_message("No roles found with those names.", ephemeral=True)
    embed = discord.Embed(title="Pick your roles", description="Click a button to add or remove a role.",
                          color=discord.Color.blurple())
    await interaction.response.send_message(embed=embed, view=RoleView(found))


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        msg = "You don't have permission to use this command."
    else:
        msg = "Something went wrong. Make sure the bot's role is high enough."
        print(error)
    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)


if not TOKEN:
    raise SystemExit("DISCORD_TOKEN is missing from the .env file.")
bot.run(TOKEN)
