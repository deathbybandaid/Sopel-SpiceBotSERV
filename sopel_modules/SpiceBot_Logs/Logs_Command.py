# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, command_permissions_check, inlist, inlist_match
from sopel_modules.SpiceBot_Events.System import bot_events_check


@sopel.module.nickname_commands('logs')
def bot_command_action(bot, trigger):

    while not bot_events_check(bot, '2004'):
        pass

    if not command_permissions_check(bot, trigger, ['admins', 'owner']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    logtype = spicemanip.main(triggerargs, 1) or None
    if not logtype or not inlist(bot, logtype, bot.memory['SpiceBot_Logs']["logs"].keys()):
        bot.osd("Current valid log(s) include: " + spicemanip.main(bot.memory['SpiceBot_Logs']["logs"].keys(), 'andlist'), trigger.sender, 'action')
        return

    logtype = inlist_match(bot, logtype, bot.memory['SpiceBot_Logs'].keys())

    if len(bot.memory['SpiceBot_Logs']["logs"][logtype]) == 0:
        bot.osd("No logs found for " + str(logtype) + ".")
        return

    bot.osd("Is Examining " + str(logtype) + " log(s).")
    for line in bot.memory['SpiceBot_Logs']["logs"][logtype]:
        bot.osd("    " + str(line))