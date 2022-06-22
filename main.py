import discord
import random
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import os
import json
from itertools import cycle
import time
import asyncio
from replit import db
from keep_alive import keep_alive  #use this only if you are using repl.it hosting

#_______________

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="s!", intents=intents)


#help remove
client.remove_command('help')

status = cycle(["With You In SIX WavE Esports", "s!help", "s!invite"])


#on
@client.event
async def on_ready():
    change_status.start()
    print("Bot is online ")


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(next(status)))


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

#Welcome
@client.event
async def on_member_join(member):
    guild = client.get_guild(756495310632648774) # YOUR INTEGER GUILD ID HERE
    welcome_channel = guild.get_channel(783703024052469772) # YOUR INTEGER CHANNEL ID HERE
    embed =discord.Embed(color=member.color)
    embed.add_field(name="New Member Joined",value=f"Hey {member.mention} ! Welcome to {member.guild.name}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_image(url="https://media1.tenor.com/images/b8a7cfdf05a6114c20a1c313b8b637cc/tenor.gif?itemid=10939070")
    await welcome_channel.send(embed=embed , content=member.mention)
    await member.send(f'We are glad to have you in the {guild.name}  Server, {member.mention} ! ')

#left
@client.event
async def on_member_remove(member:discord.Member):
  guild = client.get_guild(756495310632648774) #6wave
  left_channel = guild.get_channel(833984934075039764) #left channel id
  await left_channel.send(f'{member.mention} left the {member.guild.name} Server ! ')
 
#pings
@client.command(aliases=['check', 'test'])
async def ping(ctx):
    embed = discord.Embed(color=0x07DB9D)
    embed.add_field(name="Bot Ping",
                    value="Calculating Ping <a:mex_load:829248160010338305>")
    message = await ctx.send(embed=embed)
    await asyncio.sleep(3)

    embed4 = discord.Embed(color=0x07DB9D)
    embed4.add_field(
        name="Bot Ping",
        value=f'> **{round(client.latency*1000)}ms** , Here you go !')
    await message.edit(embed=embed4)


@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await channel.send('Channel locked.')


@client.command()
async def bon(ctx, member: discord.Member, *, reason="No Reason Given"):
    embed = discord.Embed()
    embed.add_field(
        name="Member Banned",
        value=f"{member.mention} was banned by {ctx.author.mention} | {reason}"
    )
    message = await ctx.send(embed=embed)
    await asyncio.sleep(10)
    await message.delete()


#purge
@client.command(aliases=['purge', 'clean'])
async def clear(ctx, amount=3):
    if ctx.author.guild_permissions.administrator:

        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed()
        embed.add_field(
            name='PURGE COMMAND USED',
            value=
            f'<a:trashblob:794569872997875743> | {ctx.author} PURGED {amount} messages!'
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("You need `administrator` perms to run this command")


#kick
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        if member.guild_permissions.kick_members or member.guild_permissions.ban_members or member.guild_permissions.manage_messages:
            await ctx.send(embed=discord.Embed(
                title="THE PERSON YOU ARE TRYING TO KICK IS A MOD/ADMIN"),
                           content=ctx.author.mention)
        else:
            await member.kick(reason=reason)

            embed = discord.Embed()

            embed.add_field(
                name=f'KICKED USER',
                value=
                f"<a:tick:794569296344121354> **|** *USER {member.mention} ({member.name}) HAS BEEN KICKED*"
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send(
            f'<:noperms:812683776718798889> {ctx.author.mention}, you dont have enough perms '
        )


#ban
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        if member.guild_permissions.kick_members or member.guild_permissions.ban_members or member.guild_permissions.manage_messages:
            await ctx.send(embed=discord.Embed(
                title="THE PERSON YOU ARE TRYING TO KICK IS A MOD/ADMIN"),
                           content=ctx.author.mention)
        else:
            await member.ban(reason=reason)
            embed = discord.Embed()
            embed.add_field(
                name='BANNED USER',
                value=
                f"<a:tick:794569296344121354> **|** *USER {member.mention} ({member}) HAS BEEN BANNED*"
            )

            await ctx.send(embed=embed)
    else:
        await ctx.send(
            f'<:noperms:812683776718798889> {ctx.author.mention}, you dont have enough perms '
        )


#unban
@client.command()
async def unban(ctx, *, member):
    if ctx.author.guild_permissions.ban_members:
        banned_users = await ctx.guild.bans()
        member_name, member_disriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name,
                                                   member_disriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')


#----------------------------------------------------------------------------------------------------------------------------------------------------------------


@client.command(aliases=['whois', 'infor', 'meminfo'])
async def userinfo(ctx, member: discord.Member = None):

    if ctx.author.guild_permissions.kick_members:
        member = ctx.author if not member else member

        roles = [role for role in member.roles]

        embed = discord.Embed(color=member.color,
                              timestamp=ctx.message.created_at)

        embed.set_author(name=f'USER INFO - {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Requested By {ctx.author}',
                         icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Guild Name:", value=member.display_name)
        embed.add_field(name='Member Joined at:',
                        value=member.joined_at.strftime("%a, %#d %B %Y"),
                        inline=False)
        embed.add_field(name='Account Created at:',
                        value=member.created_at.strftime("%a, %#d %B %Y"),
                        inline=False)

        embed.add_field(name=f"Roles - {len(roles) - 1}",
                        value=''.join([role.mention for role in roles]),
                        inline=False)

        embed.add_field(name='Highest Role:', value=member.top_role.mention)

        await ctx.send(embed=embed)
    else:
        await ctx.send(
            f'<:noperms:812683776718798889> {ctx.author.mention}, you need `manage members (kick)` perms to run this command !.'
        )


@client.command()
async def embed(ctx, *, qwerty):
    if ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(title=qwerty, color=0x24ffd3)

        await ctx.message.delete()

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=qwerty, color=0x24ffd3)

        await ctx.message.delete()

        message = await ctx.send(embed=embed,
                                 content='Stays only for 10 seconds')
        await asyncio.sleep(10)
        await message.delete()


@client.command(aliases=["add_r", "role+", "role +", 'addrole'])
@commands.has_permissions(administrator=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(
            f'**Gave Role to {user.display_name} (by {ctx.author})**')
    else:
        await ctx.send(
            f"{ctx.author.mention}, you need `administrator` perms to run this command!"
        )


@client.command(aliases=["remove_r", "role-", "role -"])
async def removerole(ctx, user: discord.Member, role: discord.Role):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(
            f'Removed role from **{user.display_name} (by {ctx.author})**')
    else:
        await ctx.send(
            f"{ctx.author.mention}, you need `administrator` perms to run this command!"
        )


DOGGO = [
    "https://cdn.shibe.online/shibes/47c01d4d8995d789a4f8810b3ede9115e985cb7c.jpg",
    "https://cdn.shibe.online/shibes/ecf6e5e160b0425288cd77044c1349990559dccd.jpg",
    "https://cdn.shibe.online/shibes/25f41b27e1cf8230713c16890707c787f8c33a87.jpg",
    "https://cdn.shibe.online/shibes/d266f07f3231870e451d9fe4f530ab5e36b271c5.jpg",
    "https://cdn.shibe.online/shibes/793b625781c8f3ce66fc6cbd40e534309572b182.jpg",
    "https://cdn.shibe.online/shibes/061c9865971e821f0876322439ad1775b2337da5.jpg",
    "https://cdn.shibe.online/shibes/180be33d4430fa02443b297e68ef50fdc2bf30c1.jpg",
    "https://cdn.shibe.online/shibes/9589f4ff23461f6963770aa3fb8a952bf7606243.jpg",
    "https://cdn.shibe.online/shibes/1ceca0f44498346c1d857f55d50e17c35440b39d.jpg",
    "https://cdn.shibe.online/shibes/788fee5351cc86e5971f4d4fa78c4c5f19fb1901.jpg",
    "https://cdn.shibe.online/shibes/87a2db40e2177f1ff677c7becb901d639a8af124.jpg",
    "https://cdn.shibe.online/shibes/934f806c35b4e7016fcec366200ae65583190c77.jpg",
    "https://cdn.shibe.online/shibes/985fd0749e33de808f0f4e0084a426e1ec60615e.jpg",
    "https://cdn.shibe.online/shibes/74a4c3954bde46401dd6fb6fb8a6f3cfc35de1ef.jpg",
    "https://cdn.shibe.online/shibes/bd0c317f3e770c1bc0409bc9cfa51edad343cb8d.jpg",
    "https://cdn.shibe.online/shibes/a83bffe6f6d97bc54302e40d9bdd6346b6698305.jpg",
    "https://cdn.shibe.online/shibes/c63f8cf5ab9e37a3a0eb74495471cf68ec4a4433.jpg",
    "https://cdn.shibe.online/shibes/bf88acd875c69029299e3ab68aa5e736b91d5208.jpg",
    "https://cdn.shibe.online/shibes/27de211fc1eaf2ef8ca72b700cbdfc9d74b37e69.jpg",
    "https://cdn.shibe.online/shibes/aa0d4feab645054d1cfcbf8e11fdb4f46d9a741c.jpg",
    "https://cdn.shibe.online/shibes/f1745d12fe2de5dc8f2409a622bde2de2c06564c.jpg",
    "https://cdn.shibe.online/shibes/481db896cf2ab0e297bf831893846ce5a6fa4f66.jpg",
    "https://cdn.shibe.online/shibes/f2dd318492fea00347ad16ce6fa03870bc6c4e82.jpg",
    "https://cdn.shibe.online/shibes/4fc5746d830d52fb04cadf1928521eb69c260640.jpg",
    "https://cdn.shibe.online/shibes/cefabc19d29c5fcc05ba3d248354a7bad6dba622.jpg",
    "https://cdn.shibe.online/shibes/e6eb99eb1b55392faf05a3d6382c65db6ac747ec.jpg",
    "https://cdn.shibe.online/shibes/967debc16f7d6aa726c980878783b895d1d5faee.jpg",
    "https://cdn.shibe.online/shibes/485548aa33019e9a982b13ec8264870af53404af.jpg",
    "https://cdn.shibe.online/shibes/6dd62a6f66654f87af066591cac0a3a7fd9288bd.jpg",
    "https://cdn.shibe.online/shibes/4ffe3e30fe2c22cb982e9a78c1b09dba7346cdb8.jpg",
    "https://cdn.shibe.online/shibes/013348ee96ed473c0a4be7a4674bfac8d75488d7.jpg",
    "https://cdn.shibe.online/shibes/734cecdf15b01c2355aa54a485302736d0fab2ac.jpg",
    "https://cdn.shibe.online/shibes/b3f19542d41add1cff204571c4ed11409da24af3.jpg",
    "https://cdn.shibe.online/shibes/2e1cc84e7acb51d40f736ae28215104a1de3157a.jpg",
    "https://cdn.shibe.online/shibes/bebdbba6974dfea714ea44fbe62d677173379c60.jpg",
    "https://cdn.shibe.online/shibes/700b6279b6a9c7dcc3bba0aaa12ca488e315d70c.jpg",
    "https://cdn.shibe.online/shibes/137290eba409cf689a4c2a99b07fd6cad002c1f7.jpg",
    "https://cdn.shibe.online/shibes/06a981556ff831f16cc963c3b2c4c10a40a0969c.jpg",
    "https://cdn.shibe.online/shibes/7b15383ef7243a6a253faab94928b6cbbe531a23.jpg",
    "https://cdn.shibe.online/shibes/130431562a46b67978470769ad0baf3230219954.jpg",
    "https://cdn.shibe.online/shibes/f93310233b1b4e5d0f8af74cd827def16829d944.jpg",
    "https://cdn.shibe.online/shibes/14df1df54d046f360a6013f9dab116db21092274.jpg",
    "https://cdn.shibe.online/shibes/05701c0e7bdb6dd728d6c23bb5a801fd2491e0a9.jpg",
    "https://cdn.shibe.online/shibes/98f6cce19303049678e6cc6ebcb35e7ccd4c1d99.jpg",
    "https://cdn.shibe.online/shibes/89d9d8646e5abbb8fb92f5970b50ec133e7a3226.jpg",
    "https://cdn.shibe.online/shibes/fa01249fd35a57e51b68a62dc95dd56b1b591836.jpg",
    "https://cdn.shibe.online/shibes/4d3c0f5ff576a24890c8c9b16f0aec3d7d644f82.jpg",
    "https://cdn.shibe.online/shibes/36af78b323fd9ae8f24213857d92225f5c394f4a.jpg",
    "https://cdn.shibe.online/shibes/51d9b0fa89f2c9c62523f4367d6e917881a3acdd.jpg",
    "https://cdn.shibe.online/shibes/9ed6ebf9ebc9b9fea8cf2683d8e7be3d012fd4cb.jpg",
    "https://cdn.shibe.online/shibes/48b25a82c00ed52ec94ce910144831df1e152147.jpg",
    "https://cdn.shibe.online/shibes/6e90c6acf6620e321d25c26dc979d51dab777d59.jpg",
    "https://cdn.shibe.online/shibes/777fdd4e161011c58f1d8a9e18f5a0089055ce6c.jpg",
    "https://cdn.shibe.online/shibes/a39513822b1ffa810141fe0bf94efbdd94f0a993.jpg",
    "https://cdn.shibe.online/shibes/9a065756a3f475356fedc1656b5817d301e72d17.jpg",
    "https://cdn.shibe.online/shibes/e418a0400a0dbbd9f4c133869318d6b173480217.jpg",
    "https://cdn.shibe.online/shibes/b903b7c276c70bbe81a359e609aa8e6b0ed6e44f.jpg",
    "https://cdn.shibe.online/shibes/55114f632ade009e06b4646f3682065bd957976b.jpg",
    "https://cdn.shibe.online/shibes/4e110880daf1307e9e4eec1a34f70cbbc991225b.jpg",
    "https://cdn.shibe.online/shibes/eed822f3ef60305827faaa11962f97e07ff24907.jpg",
    "https://cdn.shibe.online/shibes/b4cb419721ab855c8c4959bddb98a2c5775d1e74.jpg",
    "https://cdn.shibe.online/shibes/df6116278df5de4e714bab8fe7173e3a7017f5b8.jpg",
    "https://cdn.shibe.online/shibes/3df9a3e709f4c3f56ae7fa3f94fb49639e4f5e9e.jpg",
    "https://cdn.shibe.online/shibes/58dc76e3027387a26c9f9e94552827e5e10af76e.jpg",
    "https://cdn.shibe.online/shibes/0ec6fea4b0f660fa54d0c3d6e816b95121551870.jpg",
    "https://cdn.shibe.online/shibes/50de92632e2e9afdf8df0a023adf99838cf5bfe6.jpg",
    "https://cdn.shibe.online/shibes/8bd3d027aea34c1196dc0c1c07d09a7df5650bc2.jpg",
    "https://cdn.shibe.online/shibes/166ac2320cd0b23d66c82925005ee5b320c4a294.jpg",
    "https://cdn.shibe.online/shibes/c3d1ccbe0fa02e249cfb81c8df4094755a914c49.jpg",
    "https://cdn.shibe.online/shibes/f42828180e44c36e3a45ab2d15b8b5f598154652.jpg",
    "https://cdn.shibe.online/shibes/f043754a49b139044a4a835eb1a1ff4b3ce5f03d.jpg",
    "https://cdn.shibe.online/shibes/1914c5f997737c88b422df4c2ec23a82f52d973f.jpg",
    "https://cdn.shibe.online/shibes/25ec5b0d27e0d4601c8d04d4b5c57c7110b44b9d.jpg",
    "https://cdn.shibe.online/shibes/1a97ecc0a8ca1aaf83f11b3eb037fc63f9d32774.jpg",
    "https://cdn.shibe.online/shibes/0f8b57c669e9fbfa48a56e2e3d76c60c3078f1a3.jpg",
    "https://cdn.shibe.online/shibes/893e5cc73345192ce0ebd174353dbd47c9573d38.jpg",
    "https://cdn.shibe.online/shibes/619492e3520aa47271e6b0bef54b16c80dbd91af.jpg",
    "https://cdn.shibe.online/shibes/1fe56864286517422df28557959d497def26cbda.jpg",
    "https://cdn.shibe.online/shibes/add7158fc5ce2de6efb23b48fe285d6d97752867.jpg",
    "https://cdn.shibe.online/shibes/f8821aa8d31a377587a32228d7e45417bede923e.jpg",
    "https://cdn.shibe.online/shibes/efb08050e592cade9b49f415ffdc13649cab11cd.jpg",
    "https://cdn.shibe.online/shibes/5d39087aa2762de4b52adcd31e214b00b705b0c5.jpg",
    "https://cdn.shibe.online/shibes/e3af87c5602fe73b243d29067e43c0cc1253abbd.jpg",
    "https://cdn.shibe.online/shibes/1cb6d43776f28718fcbdc558280bc5d21dc080d7.jpg",
    "https://cdn.shibe.online/shibes/0fd8a70461c537bc3522b02cee87ef7fde05a52d.jpg",
    "https://cdn.shibe.online/shibes/679421cd41cc2a1c7a07644567394d1ca09a3e70.jpg",
    "https://cdn.shibe.online/shibes/f1961a8d99b62d6ea33d2b483bd66f994b7a1022.jpg",
    "https://cdn.shibe.online/shibes/4e19e8c3802e56fe21ebd0420cf42502ce470c92.jpg",
    "https://cdn.shibe.online/shibes/f94e056b25b51b51b3dffb9b91469f66fad524af.jpg",
    "https://cdn.shibe.online/shibes/da0abed19ae90228289b43a1f3c42f6db2fa479a.jpg",
    "https://cdn.shibe.online/shibes/1d659fbec2f1554a3bb76b37c658d09bc109e12f.jpg",
    "https://cdn.shibe.online/shibes/082a7b15aab32b32e3c55ec3da5fcb396acd1d10.jpg",
    "https://cdn.shibe.online/shibes/1540d2662b486bc11c8af76872c7fc495ed3732c.jpg",
    "https://cdn.shibe.online/shibes/d754cf14a97a6222c4cb0124c6d3d1515273de04.jpg",
    "https://cdn.shibe.online/shibes/45f3fc4551831df438e39d54af0b561cb3966ebd.jpg",
    "https://cdn.shibe.online/shibes/1284ff58f4679c79dd7802957ef49e7f6813b040.jpg",
    "https://cdn.shibe.online/shibes/14e701a7083160750f682f713ff39e82d1fabf25.jpg",
    "https://cdn.shibe.online/shibes/958b6a0ca2a8ce94acf4bdc52fddd209fa7837b1.jpg",
    "https://cdn.shibe.online/shibes/b5775659dff2534bf317f7c11b89c92cbe5df1dc.jpg",
    "https://cdn.shibe.online/shibes/62987a91dc80641e8738dea392651131cd1c5783.jpg"
]
doggo_url = random.choice(DOGGO)


@client.command(aliases=['doggo', 'Dog'])
async def dog(ctx):
    embed = discord.Embed(color=0x000000)
    embed.set_image(url=random.choice(DOGGO))
    await ctx.send(embed=embed)


@client.command(aliases=['av', 'pfp', 'AV', 'Av'])
async def avatar(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed()
    embed.set_author(name=f'AVATAR - {member}')
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f'Requested By {ctx.author}',
                     icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------------------------------------


@client.command(aliases=['serverinfo', 'si'])
async def serverstats(ctx):
    all_roles = ", ".join([str(r.mention) for r in ctx.guild.roles[1:]])
    if len(all_roles) >= 1024:
        all_roles = "NUMBERS ARE ROLES ARE MORE THAN EMBED LIMITS : )"
    else:
        all_roles = all_roles
    embed = discord.Embed(title=f"SERVER STATS FOR {ctx.guild.name}",
                          color=0x000000)
    embed.add_field(name='Owner:', value=ctx.guild.owner)
    embed.add_field(name="Total Users :",
                    value=ctx.guild.member_count,
                    inline=False)
    embed.add_field(name="Total Channels :",
                    value=len(ctx.guild.channels),
                    inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}',
                     icon_url=ctx.author.avatar_url)
    embed.add_field(name=f'Server Roles: {len(ctx.guild.roles) -1}',
                    value=all_roles,
                    inline=False)
    if ctx.guild.banner_url == True:
        texty = "** **"
    else:
        texty = "No Server Banner Found !"
    embed.add_field(name=f"Banner for : {ctx.guild.name},", value=texty)
    embed.set_image(url=ctx.guild.banner_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)

    await ctx.send(embed=embed)


@client.command()
async def membercount(ctx):

    embed = discord.Embed(color=0x000000)

    embed.add_field(
        name="Member Count",
        value=
        f"Total Members in {ctx.guild.name} : **{ctx.guild.member_count}** ")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    await ctx.send(embed=embed)


@client.command(aliases=['setnick', 'changenick', 'nickname'])
async def chnick(ctx, member: discord.Member, *, newnick):
    member = ctx.author if not member else member
    await member.edit(nick=newnick)
    embed = discord.Embed(color=0x4a8387)
    embed.add_field(name='SETNICK COMMAND USED',
                    value=f"Changed {member}'s nickname to **{newnick}**")
    await ctx.send(embed=embed)


#weather------------------------------------------------------------------------------------------------------------------------


@client.command()
async def mynick(ctx, *, nick):
    await ctx.author.edit(nick=nick)
    embed = discord.Embed(color=0x4a8387)
    embed.add_field(name="Nickname Changed",
                    value=f"Changed {ctx.author}'s nickname to {nick}")


@client.command()
async def botinfo(ctx):
    servers = list(client.guilds)
    server_count = (len(servers))
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1
    embed = discord.Embed(title="ABOUT THE BOT")
    embed.add_field(name="CLIENT ID :",
                    value="468400208200335371",
                    inline=False)
    embed.add_field(
        name="BOT OWNER INFO",
        value="DISCORD - `SHadoWNinJA#7365`  \nMENTION - <@468400208200335371>",
        inline=False)
    embed.add_field(
        name='BOT STATS:',
        value=
        f'> Bot Ping: **{round(client.latency*1000)}ms** \n> Bot Present in **{server_count} Servers**!\n> Total Members : **{members}** ',
        inline=False)
    await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def serverlist(ctx):
    servers = list(client.guilds)
    print(servers)


@client.command()
async def meme(ctx):
    irand = random.randint(0, 500)
    embed = discord.Embed()

    embed.set_image(url=f'https://ctk-api.herokuapp.com/meme/{irand}')

    await ctx.send(content=ctx.author.mention, embed=embed)


@client.command()
async def snipekill(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    snipe = ([
        'https://media1.tenor.com/images/7663c967d7f45a39ec0965afe4c6fd4f/tenor.gif?itemid=12491983',
        'https://media1.tenor.com/images/18f9732ba45d22e74c24ddc842abad08/tenor.gif?itemid=8984050'
    ])
    snipegif = random.choice(snipe)
    embed = discord.Embed()

    embed.add_field(name="** **",
                    value=f'{ctx.author.mention} **SNIPED** {member.mention}')
    embed.set_image(url=snipegif)

    await ctx.send(embed=embed)


@client.command()
async def kill(ctx, member: discord.Member = None):
    member = ctx.author if not member else member

    kill = ([
        'https://media1.tenor.com/images/f4c9636fb98360bd7df617fa44a3e66d/tenor.gif?itemid=18676892',
        'https://media1.tenor.com/images/bb4b7a7559c709ffa26c5301150e07e4/tenor.gif?itemid=9955653'
    ])
    killgif = random.choice(kill)
    embed = discord.Embed()

    embed.add_field(name='** **',
                    value=f'{ctx.author.mention} **KILLED** {member.mention}')
    embed.set_image(url=killgif)

    await ctx.send(embed=embed)


@client.command(aliases=['simprate', 'howsimp', 'simp'])
async def simpr8(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    irand = random.randint(0, 101)
    if (irand > 50):
        embed = discord.Embed(color=0xcc34eb)
        embed.add_field(name='SIMP RATE',
                        value=f'{member.mention} is **{irand}** % SIMP')
        embed.set_thumbnail(
            url=
            'https://media.discordapp.net/attachments/775671870632099851/777105392354328576/750248352049922129.png'
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xcc34eb)

        embed.add_field(name='SIMP RATE',
                        value=f'{member.mention} is **{irand}** % SIMP')
        embed.set_thumbnail(
            url=
            'https://media.discordapp.net/attachments/775671870632099851/776803540970110976/nosimp.png'
        )
        await ctx.send(embed=embed)


@client.command(aliases=['gayrate', 'howgay', 'gay'])
async def gayr8(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    irand = random.randint(0, 101)
    if (irand > 50):
        embed = discord.Embed(color=0xeb6734)
        embed.add_field(name='GAY RATE',
                        value=f'{member.mention} is **{irand}** % GAY ')
        embed.set_thumbnail(
            url=
            'https://media.discordapp.net/attachments/828623189042135050/829554867252625468/rainbowgay.gif?width=54&height=49'
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xeb6734)

        embed.add_field(name='GAY RATE',
                        value=f'{member.mention} is **{irand}** % GAY , WHEW')
        embed.set_thumbnail(
            url=
            'https://media.discordapp.net/attachments/828623189042135050/829555765022818314/image_2021-04-08_084446.png?width=41&height=41'
        )
        await ctx.send(embed=embed)


@client.command()
async def color(ctx, hexcode=None):
    if hexcode == None:
        import random
        color = "%06x" % random.randint(0, 0xFFFFFF)
        hex_o = color
    else:
        hex_o = hexcode
    embed = discord.Embed(title=f'COLOR HEX', color=0xdeeb34)
    embed.add_field(name="HEX VALUE-", value=f"{hex_o}", inline=False)

    embed.set_image(url=f"https://singlecolorimage.com/get/{hex_o}/170x170")
    embed.set_footer(text=f'Requested By {ctx.author}')
    await ctx.send(embed=embed)


@client.command()
async def doge(ctx, arguement1, *args):
    arguement2 = '+'.join(args[:])
    embed = discord.Embed(color=0xeb6734)
    embed.set_footer(text=f'Requested By :{ctx.author}',
                     icon_url=ctx.author.avatar_url)
    embed.set_image(
        url=
        f"http://apimeme.com/meme?meme=Advice-Dog&top={arguement1}&bottom={arguement2}"
    )
    await ctx.send(embed=embed)


@client.command()
async def troll(ctx, *text):
    text_use = "+".join(text)
    embed = discord.Embed()
    embed.set_footer(text=f'Requested By :{ctx.author}',
                     icon_url=ctx.author.avatar_url)
    embed.set_image(
        url=
        f'http://apimeme.com/meme?meme=Troll-Face-Colored&top=&bottom={text_use}'
    )
    await ctx.send(embed=embed)


@client.command(aliases=['lesbianrate', 'howlesbian', 'lesbo'])
async def lesbor8(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    irand = random.randint(0, 101)
    if (irand > 50):
        embed = discord.Embed()
        embed.add_field(name='LESBIAN RATE',
                        value=f'{member.mention} is **{irand}** % Lesbian ')

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed()

        embed.add_field(
            name='LESBIAN RATE',
            value=f'{member.mention} is **{irand}** % LESBIAN , WHEW')

        await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
    embed = discord.Embed(
        title='CLICK HERE TO INVITE THE BOT',
        url=
        'https://discord.com/api/oauth2/authorize?client_id=835197356076433451&permissions=0&scope=bot',
        color=0xf2f542)
    embed.add_field(name='SUPPORT SERVER -',
                    value='http://discord.gg/2HNMJK5SGH')
    await ctx.send(
        embed=embed,
        content=
        "> <:teek:807674313720987699> The bot is still in an Unverified stage , you may face issues adding the bot after it reaches a limit of 100 servers ! "
    )


@client.command(pass_context=True)
async def mute(ctx, member: discord.Member, reason='NO REASONS GIVEN'):
    if ctx.author.guild_permissions.manage_roles:

        await member.add_roles(Muted)
        embed = discord.Embed(
            title="User Muted!",
            description=
            f"**{member, ctx.message.author}** was muted by **{1}**! , REASON : {reason}",
            color=0xff00f6)
        await ctx.send(embed=embed)
    else:
        await ctx.send("You Need `manage_roles` perms to use this command!")


#help commands_______________________________________________________________________________________________________________________________________________________________

embed_man = discord.Embed(title='UTILITY COMMANDS',
                          descrption='Use these commands with prefix `m!`',
                          color=0x24ffd3)
embed_man.add_field(name='Avatar/av (Displays Avatar of a User)',
                    value='```fix\nm!av/m!avatar {USER MENTION/USER ID}\n```',
                    inline=False)
embed_man.add_field(
    name='Userinfo (Displays user information)',
    value='```fix\nm!userinfo/whois {USER MNETION/USER ID}\n```',
    inline=False)
embed_man.add_field(name='Profile (Displays Some Basic Info about an user!',
                    value='```fix\nm!profile {USER MENTION}```')
embed_man.add_field(
    name='Addrole/Removerole (ADDING/REMOVING ROLE TO A USER)',
    value=
    '```fix\nm!addrole {MEMBER MENTION /ID} {ROLE MENTION /ID}\nm!removerole {USER MENTION /ID} {ROLE MENTION\ID}```',
    inline=False)
embed_man.add_field(
    name='Timer (Sets a Timer which notifies You after time given)',
    value='```fix\nm!timer {time} {TIME UNIT} {INFO(OPTIONAL)}```',
    inline=False)
embed_man.add_field(
    name='Serverinfo (Dispalys Server info , owner , membercount etc.!)',
    value='```fix\nm!serverstats/serverinfo\n```',
    inline=False)
embed_man.add_field(
    name=
    'Setnick (Changes nickname of the mentioned user , requires `manage nickname` perms)',
    value='```fix\nm!setnick {USER MENTION} new nickname\n```',
    inline=False)
embed_man.add_field(
    name=
    'Mynick (Users with `Change Nickname` perms can change their nickname using this command)',
    value='```fix\nm!mynick (New Nickname)\n```',
    inline=False)

embed_man.add_field(
    name='Membercount (Returns the number of members in server)',
    value='```fix\nm!membercount\n```',
    inline=False)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
embed_mod = discord.Embed(title='MODERATION COMMANDS',
                          descrpition='Use these commands with prefix `s!`',
                          color=0x24ffd3)
embed_mod.add_field(name='Kick (kicks a user)',
                    value='```m!kick {MEMBER MENTION/MEMBER ID} (Reason)```',
                    inline=False)
embed_mod.add_field(name='Ban (bans a user)',
                    value='```m!ban {MEMBER MENTION/MEMBER ID} (Reason)```',
                    inline=False)
embed_mod.add_field(name='Unban (kicks a user)',
                    value='```m!unban {MEMBER MENTION/MEMBER ID}```',
                    inline=False)
embed_mod.add_field(
    name='Purge ( Deletes messages of a channel)',
    value=
    '```m!purge/=clear {number of messages to purge} , 3 messages if not mentioned limit```',
    inline=False)
embed_mod.set_footer(text='Use these commands with prefix m!')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
embed_all = discord.Embed(title='MEXTERF HELP COMMANDS',
                          color=discord.Color.green())

embed_all.set_thumbnail(
    url=
    'https://media.discordapp.net/attachments/828623189042135050/831010799932670012/e7d3ded1a01256de817a7ff16fcc164b.png'
)

embed_all.add_field(name='MODERATION COMMANDS',
                    value='```\nkick, ban, unban, purge```',
                    inline=False)
embed_all.add_field(
    name='MANAGEMENT',
    value=
    ' ```\nav \ avatar, userinfo, profile, timer, embed, setnick, mynick, serverstats, membercount```',
    inline=False)

embed_all.add_field(
    name='FUN COMMANDS',
    value='```\nsimprate, gayrate, meme, , lesbianrate, , troll, doge```',
    inline=False)
embed_all.add_field(name='DEVELOPER COMMANDS',
                    value="```\nbotinfo , ping , invite , help```",
                    inline=False)

embed_all.set_footer(
    text='Use s!help {category name} for more details about commands.')
#-------------------------------------------------------------------------------------------
embed_fun = discord.Embed()
embed_fun.set_author(name='USE THESE COMMANDS WITH PREFIX =')

embed_fun.add_field(name='Meme (A random meme)',
                    value='```fix\nm!meme```',
                    inline=False)
embed_fun.add_field(name="Simprate (Random Simp rate)",
                    value='```fix\nm!howsimp {MEMBER MENTION}```',
                    inline=False)
embed_fun.add_field(name="Gayrate (Random Gay rate)",
                    value='```fix\nm!howgay {MEMBER MENTION}```',
                    inline=False)

embed_fun.add_field(name='Doge (Text on a Doge Meme)',
                    value='```fix\nm!doge {TEXT HERE}```',
                    inline=False)
embed_fun.add_field(name='Troll (Trolling face with text)',
                    value='```fix\nm!troll {TEXT HERE}```',
                    inline=False)

embed_fun.set_footer(text='Use these command with prefix m!')
#-------------------------------------------------------------------------


@client.command(aliases=['Help', 'HELP'])
async def help(ctx, *, cat="category"):
    if cat == "management" or cat == "Management":
        message = await ctx.send(
            f"{ctx.author.mention} Loading `Management` Commands <a:mexload:825691147812864030>"
        )
        await asyncio.sleep(3)
        await message.edit(embed=embed_man, content=ctx.author.mention)

    elif cat == "mod" or cat == "Moderation" or cat == "moderation ":
        message = await ctx.send(
            f"{ctx.author.mention} Loading `Moderation` Commands <a:mexload:825691147812864030>"
        )
        await asyncio.sleep(3)
        await message.edit(embed=embed_mod, content=ctx.author.mention)

    elif cat == 'FUN' or cat == 'fun' or cat == 'Fun':
        message = await ctx.send(
            f"{ctx.author.mention} Loading `Fun` Commands <a:mexload:825691147812864030>"
        )
        await asyncio.sleep(3)
        await message.edit(embed=embed_fun, content=ctx.author.mention)
    elif cat == 'category':
        message = await ctx.send(
            f"{ctx.author.mention} Loading `Help` Commands <a:mexload:825691147812864030>"
        )
        await asyncio.sleep(3)
        await message.edit(embed=embed_all, content=ctx.author.mention)
    elif cat == "developer" or cat == 'Dev' or cat == 'Developer':
        embed = discord.Embed(
            title='NOTHING MUCH TO DESCRIBE ABOUT THESE COMMANDS : )',
            color=0x34ebde)
        await ctx.send(embed=embed)

    else:
        message = await ctx.send(
            f"{ctx.author.mention} Loading `{cat}` Commands <a:mexload:825691147812864030>"
        )
        await asyncio.sleep(1)
        await message.edit(content=f'No category named **{cat}** found !')


#____________________________________________________________________________________________________________________

keep_alive()  #only for repl.it hosting

client.run(TOKEN)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cog.{filename[:-3]}')
