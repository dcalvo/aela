import os
import json
from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


def save_data():
    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)


with open("data.json", "r") as jsonFile:
    data = json.load(jsonFile)

admin_role = "aalisa"
bot = commands.Bot(command_prefix=data["command_prefix"])


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(bot.guilds)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(error)


@bot.command(name='update', help='Don\'t use this unless you know what you\'re doing.')
@commands.dm_only()
@commands.is_owner()
async def update(ctx):
    import subprocess
    subprocess.run(["git", "pull"])
    os.execv(__file__)


@bot.command(name='confess', help='Let aela shout your confession from the rooftops')
@commands.dm_only()
async def confess(ctx):
    confession = ctx.message.content[8:].lstrip()

    embed = discord.Embed(title="I must confess:", description=confession)
    embed.set_thumbnail(url="http://pngimg.com/uploads/dog/dog_PNG50348.png")

    print(confession)
    confessional = bot.get_channel(701962929448288296)
    await confessional.send(embed=embed)


@bot.command(name='setprefix', help='Change bot\'s command prefix')
@commands.has_role(admin_role)
async def setprefix(ctx, newprefix):
    bot.command_prefix = newprefix
    data["command_prefix"] = newprefix
    save_data()
    await ctx.send(f"New prefix set: {newprefix}")


@bot.command(name='setavatar', help='Change bot\'s avatar')
@commands.has_role(admin_role)
async def setavatar(ctx, url):
    from urllib import error
    from urllib import request
    from urllib.parse import urlparse
    import urllib.request
    from os.path import splitext

    def get_ext(url):
        """Return the filename extension from url, or ''."""
        parsed = urlparse(url)
        root, ext = splitext(parsed.path)
        return ext  # or ext[1:] if you don't want the leading '.'

    try:
        ext = get_ext(url)
        if ext != ".jpg" and ext != ".png":
            raise TypeError

        resource = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})  # to get around bot blocking
        img = request.urlopen(resource).read()
        await bot.user.edit(avatar=img)
        await ctx.send("Avatar successfully changed.")
    except TypeError:
        await ctx.send("Unsupported file type. Only .png or .jpg are supported.")
    except discord.HTTPException:
        await ctx.send("You are changing your avatar too fast. Try again later.")
    except urllib.error.HTTPError as e:
        await ctx.send(e)


bot.run(TOKEN)