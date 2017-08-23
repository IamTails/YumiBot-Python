import discord
from discord.ext import commands
import datetime
import time
import platform
import asyncio
import logging
import traceback
import sys

description = """ some desc here. """
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = setup_logger('yumi')
help_attrs = dict(hidden=True)
bot = commands.Bot(command_prefix="/y", description=description, help_attrs=help_attrs)
initial_extensions = []
botVersion = "1.0.0_DEV"
errchid = "some ch id"
#guild log
glid = "someid"
@bot.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    server = ctx.message.server
    if isinstance(error, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.DisabledCommand):
        await ctx.bot.send_message(channel, "That command is disabled.")
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
        oneliner = "Error in command '**__{}__**' - `{}`: `{}`".format(
            ctx.command.qualified_name, type(error.original).__name__,
            str(error.original))
        em = discord.Embed(title="**Error** :x:", description="Error in command",color=discord.Color.red())
        em.add_field(name="traceback", value=oneliner)
        await ctx.bot.send_message(channel, embed=em)
        echan = bot.get_channel(errchid)
        await ctx.bot.send_message(echan, oneliner +'\n' + '**On channel** : '+ channel.name + '\n'+ "**On server** : " + server.name + "  **id** : "+ server.id)

    elif isinstance(error, commands.CommandOnCooldown):
        pass
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(channel, "Nope that command is not "
                                        "available in DMs.")
    else:
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
        oneliner = "Error in command '{}' - {}: {}".format(
            ctx.command.qualified_name, type(error.original).__name__,
            str(error.original))
        echan = bot.get_channel(errchid)
        await ctx.bot.send_message(echan, oneliner + 'on channel :'+ channel.name + "on server :" + server.name + "id :"+ server.id )

@bot.event
async def on_ready():
    await update()
    print("Loading YumiBot...")
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('oauth link:')
    print(discord.utils.oauth_url(bot.user.id))
    print("Servers",str(len(bot.servers)))
    print("Users",str(len(set(bot.get_all_members()))))
    servers = str(len(bot.servers))
    users = str(len(set(bot.get_all_members())))
    message = '/yhelp | {} servers | {} users'.format(servers, users)
    game = discord.Game(name=message)
    await bot.change_presence(game=game)
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()
    print("====================")

@bot.command(pass_context=True)
async def ping(ctx):
    try:
        before = datetime.datetime.utcnow()
        ping_msg = await bot.send_message(ctx.message.channel, content=":mega: **Pinging...**")
        ping = (datetime.datetime.utcnow() - before) * 1000
        before2 = time.monotonic()
        await (await bot.ws.ping())
        after = time.monotonic()
        ping2 = (after - before2) * 1000
        await bot.edit_message(ping_msg, new_content=":mega: Pong! The message took **{:.2f}ms**!".format(ping.total_seconds())+" `Websocket: {0:.0f}ms` :thinking:".format(ping2))
    except Exception as e:
        await bot.say("{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(ctx.message.author, e, bot.command_prefix))

@bot.command(pass_context = True)
async def about(ctx):
    try:
        server_count = 0
        member_count = 0
        for server in bot.servers:
            server_count += 1
            for member in server.members:
                member_count += 1
        embed = discord.Embed(title='About Yumi!', description = "Nothing to see here.", color=ctx.message.author.color).add_field(name='Version Number', value=str(botVersion), inline=False).add_field(name='Servers', value=str(server_count)).add_field(name='Users',value=str(member_count) + '\n\nJoin the [support guild](https://discord.gg/T2pyUvf)', inline=False).set_footer(text="Made with love <3").set_thumbnail(url=ctx.message.server.me.avatar_url)
        await bot.send_message(ctx.message.channel, content=None, embed=embed)
    except Exception as e:
        await bot.say("{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(ctx.message.author, e, bot.command_prefix))

@bot.command(pass_context=True)
async def info(ctx):
    try:
        commands = len(bot.commands)
        dpyVersion = discord.__version__
        pyVersion = platform.python_version()
        server_count = 0
        member_count = 0
        for server in bot.servers:
            server_count += 1
            for member in server.members:
                member_count += 1
        em = discord.Embed(title="Information",color=ctx.message.author.color)
        em.add_field(name="Versions",value="**Bot**: {0}\n**DiscordPY**: {1}\n**Python**: {2}".format(botVersion, dpyVersion, pyVersion),inline=False)
        em.add_field(name="Bot",value="**Commands**: {0}\n**Guilds:** {1}\n**Users**: {2}".format(commands, server_count, member_count),inline=False)
        await bot.send_message(ctx.message.channel, content=None, embed=em)
    except Exception as e:
        await bot.say("{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(ctx.message.author, e, bot.command_prefix))

        
@bot.event
async def on_server_join(server):
    mirror = bot.get_channel(glid)
    invite = await bot.create_invite(server)
    em = discord.Embed(title="New Server Added", color=discord.Color.green())
    avatar = bot.user.avatar_url if bot.user.avatar else bot.user.default_avatar_url
    em.set_author(name=server.name, icon_url=avatar)
    em.set_thumbnail(url=server.icon_url)
    em.add_field(name="Total users", value=len(server.members))
    em.add_field(name="Invite Link", value=invite)
    em.add_field(name="Server Owner", value=str(server.owner))
    em.add_field(name="Total servers", value=len(bot.servers))
    em.set_footer(text="Server ID: " + server.id)
    await bot.send_message(mirror, embed=em)
    servers = str(len(bot.servers))
    users = str(len(set(bot.get_all_members())))
    message = '/yhelp | {} servers | {} users'.format(servers, users)
    game = discord.Game(name=message)
    await bot.change_presence(game=game)


@bot.event
async def on_server_remove(server):
    mirror = bot.get_channel(glid)
    em = discord.Embed(title="Server Left", color=discord.Color.red())
    avatar = bot.user.avatar_url if bot.user.avatar else bot.user.default_avatar_url
    em.set_author(name=server.name, icon_url=avatar)
    em.set_thumbnail(url=server.icon_url)
    em.add_field(name="Total servers", value=len(bot.servers))
    em.add_field(name="Owner", value=str(server.owner))
    em.set_footer(text="Server ID: " + server.id)
    await bot.send_message(mirror, embed=em)
    servers = str(len(bot.servers))
    users = str(len(set(bot.get_all_members())))
    message = '/yhelp | {} servers | {} users'.format(servers, users)
    game = discord.Game(name=message)
    await bot.change_presence(game=game)

        
async def update():

    payload = json.dumps({
        'server_count': len(bot.servers)
    })

    headers = {
        'authorization': 'Your Key',
        'content-type': 'application/json'
    }

    headers2 = {
        'authorization': 'Your Key',
        'content-type': 'application/json'
    }

    DISCORD_BOTS_API = 'https://bots.discord.pw/api'
    Oliy_api = 'https://discordbots.org/api'

# discordbots.org
    url = '{0}/bots/317145148901556234/stats'.format(Oliy_api)
    async with session.post(url, data=payload, headers=headers2) as resp:
        logger.info('SERVER COUNT UPDATED.\ndiscordbots.org statistics returned {0.status} for {1}\n'.format(resp, payload))

# bots.discord.pw
    url = '{0}/bots/317145148901556234/stats'.format(DISCORD_BOTS_API)
    async with session.post(url, data=payload, headers=headers) as resp:
        logger.info('SERVER COUNT UPDATED.\nbots.discord.pw statistics returned {0.status} for {1}\n'.format(resp, payload))
        
if __name__ == '__main__':
    bot.log = setup_logger('')
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    bot.counter = Counter()
    bot.run(token)
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
