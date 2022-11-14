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

    cmd, body = parse_command(message.content)

    if cmd == '!cmb':
        rsn = body

        levels = calc_cmb_lvl(rsn)

        response = '{} has a combat level of {}\n' \
                   'Attack:    {:<2}\n' \
                   'Defence:   {:<2}\n' \
                   'Strength:  {:<2}\n' \
                   'Hitpoints: {:<2}\n' \
                   'Ranged:    {:<2}\n' \
                   'Prayer:    {:<2}\n' \
                   'Magic:     {:<2}\n'.format(rsn, levels[0],
                                               levels[1],
                                               levels[2],
                                               levels[3],
                                               levels[4],
                                               levels[5],
                                               levels[6],
                                               levels[7])

        await message.channel.send(response)
        print(f'Message sent: "{response}"/n')

    elif cmd == '!hs':
        rsn = body

        get_hs(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Highscores:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!skills':
        rsn = body

        get_skills(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Skills:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!bosses':
        rsn = body

        get_bosses(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Boss KC:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!ehb':
        rsn = body

        calc_ehb(rsn)

        file = rsn + '_ehb.txt'
        file_payload = discord.File(file, filename=(rsn + '_ehb.txt'))
        await message.channel.send(f'{rsn}\'s OSRS efficient hours bossed:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!activities':
        rsn = body

        get_activities(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Activities:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!:p':
        await message.channel.send(':stuck_out_tongue_winking_eye:\n'
                                   '***__THBBBBBBBBBBBBBBBT!!!!__***')

    elif cmd == '!version':
        await message.channel.send(f'Running Clockwork Penguin {VERSION}\n')


def parse_command(content):
    if ' ' not in content:
        return content.lower(), ''
    else:
        cmd, body = content.split(' ', maxsplit=1)
        return cmd.lower(), body


client.run(TOKEN)
