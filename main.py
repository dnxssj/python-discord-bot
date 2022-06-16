import discord
from discord.ext import commands

import json
import os

if os.path.exists(os.getcwd() + "/config.json"):
    
    with open("./config.json") as f:
        configData = json.load(f)

else: 
    configTemplate = {"Token": "", "Prefix": ">"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command(description="Mutes an specific user")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_messages_history=False, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} has been muted for {reason}")
    await member.send(f"You have been muted in the server {guild.name} for {reason}")

@bot.command(description="Unmutes muted user")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"{member.mention} unmuted")
    await member.send(f"You have been unmuted in the server {ctx.guild.name}")

@bot.command(description="Kicks an specific user")
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason = reason)
    await ctx.send(f"{member.mention} has been kicked for {reason}")

@bot.command(description="Bans an specific user")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason = reason)
    await ctx.send(f"{member.mention} has been banned for {reason}")

@bot.command(description="User unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discriminator = member.split("#")

    for ban in bannedUsers:
        user = ban.user

        if(user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned")
            return
    


bot.run(token)