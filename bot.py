import discord
from discord.ext import commands
import asyncio

prefix = "!"
bot = commands.Bot(command_prefix=prefix)
print('[Init] Bot configuré !')

@bot.event
async def on_ready():
    print("[Init] Bot en ligne !")
    await bot.change_presence(activity=discord.Game("Ouais ouais ouais"))
    
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "?":
        await message.channel.send("Ouais ouais ouais !")
    await bot.process_commands(message)
	
    
bot.run("NjI3MTEwMzM1ODAyNzY5NDA4.XY34wA.ksGsiEaAlgzbZlYVldLSrjivmKM")