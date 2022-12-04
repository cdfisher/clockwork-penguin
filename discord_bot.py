"""discord_bot.py
Main file for the Clockwork Penguin Discord bot
Contains event handlers, command parser and list of
commands/responses.
"""

import os

import discord

from config import *
from osrs_utils import *


# If in test mode, use test values for token, guild, and webhooks
if TEST_MODE:
    TOKEN = TEST_TOKEN
    GUILD = TEST_GUILD
    WH = TEST_WEBHOOK
else:
    TOKEN = DISCORD_TOKEN
    GUILD = DISCORD_GUILD
    WH = BIRDMEN_WEBHOOK

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
        # If the required argument is missing, stop here
        if len(body) == 0:
            return
        rsn = body

        levels = calc_cmb_lvl(rsn)

        if levels[0] == [-1]:
            response = f'User {rsn} not found!'
        elif levels[0] == [-2]:
            response = f'Cannot calculate user {rsn}\'s combat' \
                       f'level as not all skills are listed on the highscores.\n'
        else:
            embed = discord.Embed(title=rsn + "\'s Combat level:", description=levels[0], color=0xff0000)
            embed.add_field(name="Attack", value=levels[1])
            embed.add_field(name="Defence", value=levels[2])
            embed.add_field(name="Strength", value=levels[3])
            embed.add_field(name="Hitpoints", value=levels[4])
            embed.add_field(name="Ranged", value=levels[5])
            embed.add_field(name="Prayer", value=levels[6])
            embed.add_field(name="Magic", value=levels[7])

        await message.channel.send(embed=embed)

    elif cmd == '!hs':
        # If the required argument is missing, stop here
        if len(body) == 0:
            return

        rsn = body
        get_hs(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Highscores:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!skills':
        # If the required argument is missing, stop here
        if len(body) == 0:
            return

        rsn = body
        get_skills(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Skills:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!bosses':
        # If the required argument is missing, stop here
        if len(body) == 0:
            return
        rsn = body

        get_bosses(rsn)

        file = rsn + '.txt'
        file_payload = discord.File(file, filename=(rsn + '.txt'))
        await message.channel.send(f'{rsn}\'s OSRS Boss KC:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!ehb':
        # If the required argument is missing, stop here
        if len(body) == 0:
            return

        rsn = body
        calc_ehb(rsn)

        file = rsn + '_ehb.txt'
        file_payload = discord.File(file, filename=(rsn + '_ehb.txt'))
        await message.channel.send(f'{rsn}\'s OSRS efficient hours bossed:\n', file=file_payload)
        os.remove(file)

    elif cmd == '!activities':
        # If the required argument is missing, stop here
        if len(body) == 0:
            return

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

    elif cmd == '!birdmen':
        file_payload = discord.File('resources/birdman.png', filename='resources/birdman.png')
        hook = discord.Webhook.from_url(WH, adapter=discord.RequestsWebhookAdapter())
        hook.send(content='#birdmen!\n ***S C R E E E E E***\n', file=file_payload)
        # file = {'birdman.png': open('birdman.png', 'rb')}
        # data = {
        #     'content': '#birdmen!\n ***S C R E E E E E***\n'
        # }
        #
        # result = requests.post(WH, json=data, files=file)
        # try:
        #     result.raise_for_status()
        # except requests.exceptions.HTTPError as err:
        #     print(err)
        # else:
        #     print(f'Payload delivered with code {result.status_code}\n')
    elif cmd == '!christmas-cracker':
        user_1, user_2 = body.split('+', maxsplit=1)
        users = [user_1, user_2]
        winner = np.random.choice(users)
        users.remove(winner)
        loser = users[0]

        color = partyhat()
        other_prize = cc_other_prize()
        msg = f'{winner} got a {color} partyhat! Sweet!\n' \
              f'{loser} got {other_prize}. Scam game!\n'

        file = color + '_partyhat.png'
        filepath = 'resources/' + file
        file_payload = discord.File(filepath, filename=file)
        await message.channel.send(msg, file=file_payload)


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
