# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun.prerun('nickname')
@sopel.module.nickname_commands('update')
def nickname_comand_update(bot, trigger):

    if not SpiceBot.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.osd("I was unable to process this Bot Nick command due to privilege issues.")
        return

    if not len(trigger.sb['args']):
        commandused = 'nodeps'
    else:
        commandused = spicemanip.main(trigger.sb['args'], 1).lower()

    if commandused not in ['deps', 'nodeps']:
        bot.osd("Please specify deps or nodeps")
        return

    trigger.sb['args'] = spicemanip.main(trigger.sb['args'], '2+', 'list')

    quitmessage = "Received command from " + trigger.nick + " to update from Github and restart"
    SpiceBot.logs.log('SpiceBot_Update', quitmessage)
    bot.osd(quitmessage, list(bot.channels.keys()))

    if commandused == 'nodeps':
        SpiceBot.spicebot_update(False)
    if commandused == 'deps':
        SpiceBot.spicebot_update(True)

    # service_manip(bot.nick, 'restart', 'SpiceBot_Update')
    SpiceBot.spicebot_reload(bot, 'SpiceBot_Update', quitmessage)


@sopel.module.nickname_commands('restart')
def nickname_comand_restart(bot, trigger):

    if not trigger.admin:
        bot.osd("You are not authorized to perform this function.")

    quitmessage = "Received command from " + trigger.nick + " to restart. Be Back Soon!"
    SpiceBot.logs.log('SpiceBot_Restart', quitmessage)
    bot.osd(quitmessage, list(bot.channels.keys()))

    # service_manip(bot.nick, 'restart', 'SpiceBot_Restart')
    SpiceBot.spicebot_reload(bot, 'SpiceBot_Restart', quitmessage)