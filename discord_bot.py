import discord
import os

from config import *
from osrs_utils import *

TOKEN = DISCORD_TOKEN
GUILD = DISCORD_GUILD

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} has connected to the following server:\n'
        f'{guild.name} (id: {guild.id})'
    )


@client.event
async def on_message(message):
    # If the bot sent a message, ignore it
    if message.author == client.user:
        return

    if message.content.lower()[:4] == '!cmb':
        rsn = message.content[5:]

        levels = calc_cmb_lvl(rsn)

        response = '{} has a combat level of {}\n' \
                   'Attack: {}\n' \
                   'Defence: {}\n' \
                   'Strength: {}\n' \
                   'Hitpoints: {}\n' \
                   'Ranged: {}\n' \
                   'Prayer: {}\n' \
                   'Magic: {}\n'.format(rsn, levels[0],
                                        levels[1],
                                        levels[2],
                                        levels[3],
                                        levels[4],
                                        levels[5],
                                        levels[6],
                                        levels[7])

        await message.channel.send(response)
        print(f'Message sent: "{response}"/n')

    elif message.content.lower()[:3] == '!hs':
        rsn = message.content[4:]

        get_hs(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn+'.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Highscores:\n', file=file_payload)
        os.remove(file)

    elif message.content.lower()[:7] == '!skills':
        rsn = message.content[8:]

        get_skills(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Skills:\n', file=file_payload)
        os.remove(file)

    elif message.content.lower()[:7] == '!bosses':
        rsn = message.content[8:]

        get_bosses(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Boss KC:\n', file=file_payload)
        os.remove(file)

    elif message.content.lower()[:4] == '!ehb':
        rsn = message.content[5:]

        calc_ehb(rsn)

        file = rsn + '_ehb.txt'
        file_payload = discord.File(file, filename=(rsn + '_ehb.txt'))
        await message.channel.send(f'{rsn}\'s OSRS efficient hours bossed:\n', file=file_payload)
        os.remove(file)

    elif message.content.lower()[:11] == '!activities':
        rsn = message.content[12:]

        get_activities(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Activities:\n', file=file_payload)
        os.remove(file)

    elif message.content.lower()[:3] == '!:p':
        await message.channel.send(':stuck_out_tongue_winking_eye:\n'
                                   '***__THBBBBBBBBBBBBBBBT!!!!__***')

    elif message.content.lower()[:8] == '!version':
        await message.channel.send(f'Running Clockwork Penguin {VERSION}\n')


client.run(TOKEN)
