import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import asyncio
import random
import os
from flask import Flask
from threading import Thread

# -------------------
# FLASK KEEP-ALIVE
# -------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Loey the Coal Miner is mining coal ⛏️"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------------------
# DISCORD BOT SETUP
# -------------------
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# Level Titles
LEVEL_TITLES = [
    "Amateur 🥉",
    "Novice",
    "Apprentice",
    "Adept",
    "Skilled",
    "Specialist",
    "Expert",
    "Virtuoso",
    "Master",
    "Grandmaster 🏆"
]

user_xp = {}
level_threshold = 100  # XP per level


# -------------------
# BOT EVENTS
# -------------------
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and mining coal!")
    await bot.change_presence(activity=discord.Game(name="⛏️ Mining in The Coal Mines"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user = message.author
    user_xp[user.id] = user_xp.get(user.id, 0) + random.randint(5, 15)

    xp = user_xp[user.id]
    level = xp // level_threshold

    if xp % level_threshold < 10 and xp > 0:  # simple level up check
        level_title = LEVEL_TITLES[min(level, len(LEVEL_TITLES)-1)]
        await message.channel.send(f"🎉 {user.mention} has reached **Level {level + 1} - {level_title}!**")

    await bot.process_commands(message)


# -------------------
# MODERATION COMMANDS
# -------------------
@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} has been kicked. Reason: {reason}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("❌ You don't have permission to kick members.")

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} has been banned. Reason: {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("❌ You don't have permission to ban members.")

@bot.command()
@has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
    duration = discord.utils.utcnow() + timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"⏳ {member} has been timed out for {minutes} minutes.")


# -------------------
# FUN / ENTERTAINMENT COMMANDS
# -------------------
@bot.command()
async def mine(ctx):
    ores = ["Coal", "Iron", "Gold", "Diamond", "Emerald"]
    found = random.choice(ores)
    await ctx.send(f"⛏️ {ctx.author.mention} mined some **{found}!**")

@bot.command()
async def joke(ctx):
    jokes = [
        "Why did the miner go to therapy? He had too much 'ore'-pression.",
        "Coal miners have the deepest jobs!",
        "I asked Loey for diamonds... he gave me coal 😭"
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🪓 Loey the Coal Miner Commands", color=discord.Color.gold())
    embed.add_field(name="⚙️ Moderation", value="`!kick`, `!ban`, `!timeout`", inline=False)
    embed.add_field(name="🎮 Fun", value="`!mine`, `!joke`", inline=False)
    embed.add_field(name="📈 Level System", value="Earn XP by chatting and level up!", inline=False)
    embed.set_footer(text="Developed for The Coal Mines ⛏️")
    await ctx.send(embed=embed)


# -------------------
# RUN BOT
# -------------------
keep_alive()
bot.run(os.getenv("TOKEN"))
