"""discord_bot.py
Main file for the Clockwork Penguin Discord bot
Contains event handlers, command parser and list of
commands/responses.
"""

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
    """On message event in Discord server, checks if message contains
    a command, and if so executes that command.

    :param message: Message sent in server
    :return: None
    """

    # Ignore messages that this bot sent itself
    if message.author == client.user:
        return

    # If message is not a command, don't do anything else
    if message.content[0] != '!':
        return

    # Break out message into command
    cmd, body = parse_command(message.content)

    # if/elif tree that handles all commands
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
    """Breaks message.content into command and body of arguments

    :param content: string message.content to parse
    :return: string cmd, string body. If content has no arguments,
    body returns an empty string.
    """
    if ' ' not in content:
        return content.lower(), ''
    else:
        cmd, body = content.split(' ', maxsplit=1)
        return cmd.lower(), body


client.run(TOKEN)
