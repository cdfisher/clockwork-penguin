"""osrs_utils.py
Various OSRS-related utility functions.
"""
import numpy as np
from math import floor
from hs_wrapper import *

"""EHB_RATES:
    Dict of bosses and their respective kills per efficient bossing hour.
    EHB_RATES(boss) returns a tuple of length 2 as a key.
    key[0] is the EHB rate for main accounts, and key[1] is the rate for ironman accounts.
    A rate value of -1.0 indicates boss kills do not count toward EHB for that account type.
    Rates have been sourced from https://wiseoldman.net/rates/ehb
    """
EHB_RATES = {'abyssal_sire': (42.0, 32.0),
             'alchemical_hydra': (27.0, 26.0),
             'barrows_chests': (-1.0, 18.0),
             'bryophyta': (-1.0, 9.0),
             'callisto': (50.0, 30.0),
             'cerberus': (61.0, 54.0),
             'chambers_of_xeric': (3.0, 2.8),
             'chambers_of_xeric_challenge_mode': (2.2, 2.0),
             'chaos_elemental': (60.0, 48.0),
             'chaos_fanatic': (100.0, 80.0),
             'commander_zilyana': (55.0, 25.0),
             'corporeal_beast': (50.0, 6.5),
             'crazy_archaeologist': (-1.0, 75.0),
             'dagannoth_prime': (88.0, 88.0),
             'dagannoth_rex': (88.0, 88.0),
             'dagannoth_supreme': (88.0, 88.0),
             'deranged_archaeologist': (-1.0, 80.0),
             'general_graardor': (50.0, 25.0),
             'giant_mole': (100.0, 80.0),
             'grotesque_guardians': (36.0, 31.0),
             'hespori': (-1.0, 60.0),
             'kalphite_queen': (50.0, 30.0),
             'king_black_dragon': (120.0, 70.0),
             'kraken': (90.0, 82.0),
             'kree_arra': (25.0, 22.0),
             'kril_tsutsaroth': (65.0, 26.0),
             'mimic': (-1.0, 60.0),
             'nex': (12.0, 12.0),
             'nightmare': (14.0, 11.0),
             'phosanis_nightmare': (7.5, 6.5),
             'obor': (-1.0, 12.0),
             'phantom_muspah': (25.0, 25.0),
             'sarachnis': (80.0, 56.0),
             'scorpia': (130.0, 60.0),
             'skotizo': (45.0, 38.0),
             'tempoross': (-1.0, -1.0),
             'the_gauntlet': (10.0, 10.0),
             'the_corrupted_gauntlet': (6.5, 6.5),
             'theatre_of_blood': (3.0, 2.5),
             'theatre_of_blood_hard_mode': (3.0, 2.4),
             'thermonuclear_smoke_devil': (125.0, 80.0),
             'tombs_of_amascut': (2.5, 2.5),
             'tombs_of_amascut_expert_mode': (2.0, 2.0),
             'tzkal_zuk': (0.8, 0.8),
             'tztok_jad': (2.0, 2.0),
             'venenatis': (50.0, 35.0),
             'vet_ion': (30.0, 23.0),
             'vorkath': (32.0, 32.0),
             'wintertodt': (-1.0, -1.0),
             'zalcano': (-1.0, -1.0),
             'zulrah': (35.0, 32.0)}


def get_ehb(boss, kc, mode):
    """ Returns EHB value for a given boss.

    :param boss: string from BOSSES in hs_wrapper.py denoting all tracked bosses
    :param kc: int, player's kill count for :parameter boss
    :param mode: str with value 'main' or 'iron', denoting which set of rates to use
    :return: float representing player's efficient hours spent at :parameter boss
    """
    if mode == 'main':
        return kc / EHB_RATES[boss][0]
    elif mode == 'iron':
        return kc / EHB_RATES[boss][1]
    else:
        print(f'{mode} not recognized\n')


def calc_ehb(rsn):
    """Calculates a player's efficient hours bossed and writes to a text file.

    :param rsn: str value of a player's OSRS username
    :return: None, creates file {rsn}_ehb.txt to be sent as message attachment
    """
    try:
        iron = is_iron(rsn)
    except ValueError:
        return f'User {rsn} not found!\n'

    if iron:
        mode = 'iron'
        mode_str = 'Using Ironman EHB rates\n'
    else:
        mode = 'main'
        mode_str = 'Using main account EHB rates\n'
    total_ehb = 0.0
    outfile = rsn + '_ehb.txt'
    user = get_user(rsn)
    with open(outfile, 'w') as file:
        file.write(f'{rsn}\'s OSRS efficient hours bossed:\n'
                   f'{mode_str}'
                   f'----------------------------------------------------------\n')

        for i in range(len(BOSSES)):
            kc = query_boss_kc(user, BOSSES[i])
            ehb = get_ehb(BOSSES[i], kc, mode)
            if (kc > 0) & (ehb > 0):
                file.write(f'{FORMATTED_BOSSES[i]:<34}: {kc:>7} KC {round(ehb, 1):>7} EHB\n')
                total_ehb += ehb

        file.write('Total: {:>7} EHB\n'.format(round(total_ehb, 2)))

        file.close()


def is_iron(rsn):
    """Checks if a given player is an Ironman account.

    :param rsn: str value of a player's OSRS username
    :return: boolean, True if user is an ironman, False if not
    @:raises ValueError if player is not found on highscores
    """
    # If we find a user on the Ironman highscores, we know they're an ironman.
    # Otherwise, we check to make sure the user exists on the main highscore board
    # This isn't a great solution but it's really the only way to check an account's status
    try:
        user = Highscores(rsn, target='ironman')
        return True
    except ValueError:
        try:
            user = Highscores(rsn)
            return False
        except ValueError:
            raise ValueError


def calc_cmb_lvl(rsn):
    """Calculates player's combat level.

    :param rsn: str value of a player's OSRS username
    :return: array levels of length 8 containing player's combat level and all related levels
    """
    try:
        user = Highscores(rsn)
    except ValueError:
        return [-1]

    attack = user.attack.level
    defence = user.defence.level
    strength = user.strength.level
    hitpoints = user.hitpoints.level
    ranged = user.ranged.level
    prayer = user.prayer.level
    magic = user.magic.level

    if ((attack == -1) or (defence == -1) or (strength == -1) or (hitpoints == -1) or
            (ranged == -1) or (prayer == -1) or (magic == -1)):
        return [-2]

    base_lvl = round((0.25 * (float(defence) + float(hitpoints) + floor((float(prayer) * 0.5)))), 4)
    melee_lvl = round((13 / 40) * (float(attack) + float(strength)), 4)
    range_lvl = round((13 / 40) * floor((float(ranged) * (3 / 2))), 4)
    mage_lvl = round((13 / 40) * floor((float(magic) * (3 / 2))), 4)

    final_lvl = floor(base_lvl + max(melee_lvl, range_lvl, mage_lvl))

# Partial combat levels as seen in Runelite
#    final_lvl = base_lvl + max(melee_lvl, range_lvl, mage_lvl)

    levels = [final_lvl, attack, defence, strength, hitpoints, ranged, prayer, magic]
    return levels


def get_hs(rsn):
    """Writes all highscores entries for a player to file {rsn}.txt

    :param rsn: str value of a player's OSRS username
    :return: None, writes to file {rsn}.txt
    """
    outfile = rsn + '.txt'
    user = get_user(rsn)
    with open(outfile, 'w') as file:
        file.write('{}\'s OSRS Highscores:\n'
                   '\nLevels:\n'
                   '---------------------------------------------------\n'.format(rsn))

        for i in range(len(SKILLS)):
            lvl = query_skill_level(user, SKILLS[i])
            xp = query_skill_xp(user, SKILLS[i])
            if lvl > 0:
                file.write('{:<12}: Level: {:>5} XP: {:>10}\n'.format(FORMATTED_SKILLS[i], lvl, xp))

        file.write('\nActivities:\n'
                   '---------------------------------------------------\n')

        for i in range(len(ACTIVITIES)):
            score = query_activity_score(user, ACTIVITIES[i])
            if score > 0:
                file.write('{:<24}: {:>6}\n'.format(FORMATTED_ACTIVITIES[i], score))

        file.write('\nBosses:\n'
                   '---------------------------------------------------\n')

        for i in range(len(BOSSES)):
            kc = query_boss_kc(user, BOSSES[i])
            if kc > 0:
                file.write('{:<34}: {:>7} KC\n'.format(FORMATTED_BOSSES[i], kc))

        file.close()


def get_skills(rsn):
    """Writes all of a player's levels to file {rsn}.txt, provided each level is listed
    on the OSRS Highscores.

    :param rsn: str value of a player's OSRS username
    :return: None, writes to file {rsn}.txt
    """
    outfile = rsn + '.txt'
    user = get_user(rsn)
    with open(outfile, 'w') as file:
        file.write('{}\'s OSRS Skillss:\n'
                   '\nLevels:\n'
                   '---------------------------------------------------\n'.format(rsn))

        for i in range(len(SKILLS)):
            lvl = query_skill_level(user, SKILLS[i])
            xp = query_skill_xp(user, SKILLS[i])
            if lvl > 0:
                file.write('{:<12}: Level: {:>5} XP: {:>10}\n'.format(FORMATTED_SKILLS[i], lvl, xp))

        file.close()


def get_activities(rsn):
    """Writes all of a player's activity scores to file {rsn}.txt, provided they are
    listed on the OSRS Highscores for each activity.

    :param rsn: str value of a player's OSRS username
    :return: None, writes to file {rsn}.txt
    """
    outfile = rsn + '.txt'
    user = get_user(rsn)
    with open(outfile, 'w') as file:
        file.write('{}\'s OSRS Activities:\n'
                   '---------------------------------------------------\n'.format(rsn))

        for i in range(len(ACTIVITIES)):
            score = query_activity_score(user, ACTIVITIES[i])
            if score > 0:
                file.write('{:<24}: {:>6}\n'.format(FORMATTED_ACTIVITIES[i], score))

        file.close()


def get_bosses(rsn):
    """Writes all of a player's boss kill counts to file {rsn}.txt, provided they are
    listed on the OSRS Highscores for each boss.

    :param rsn: str value of a player's OSRS username
    :return: None, writes to file {rsn}.txt
    """
    outfile = rsn + '.txt'
    user = get_user(rsn)
    with open(outfile, 'w') as file:
        file.write('{}\'s OSRS Boss KC:\n'
                   '---------------------------------------------------\n'.format(rsn))

        for i in range(len(BOSSES)):
            kc = query_boss_kc(user, BOSSES[i])
            if kc > 0:
                file.write('{:<34}: {:>7} KC\n'.format(FORMATTED_BOSSES[i], kc))

        file.close()


def partyhat():
    """Returns a string of a random color that aligns with the drop rate of each color partyhat
    from a Christmas cracker"""
    colors = ['red', 'yellow', 'white', 'green', 'blue', 'purple']
    color_weights = [0.25, 0.22, 0.18, 0.16, 0.12, 0.07]
    return np.random.choice(colors, p=color_weights)


def cc_other_prize():
    """Returns a string matching with a prize from the Christmas cracker's 'Other' drop
    table, weighted appropriately."""
    items = ['a chocolate bar', 'a silver bar', 'a chocolate cake', 'a spinach roll',
             '5 noted iron ore', 'a gold ring', 'a piece of silk', 'a holy symbol',
             'a black dagger', 'a Law rune']
    item_weights = [0.188, 0.140, 0.125, 0.125, 0.109, 0.078, 0.078, 0.078, 0.048, 0.031]
    return np.random.choice(items, p=item_weights)
